# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Deprecated by socorro/external/postgresql/service_base.py"""

import contextlib
import logging

import psycopg2

from socorrolib.lib import DatabaseError

from socorro.external.postgresql.dbapi2_util import (
    execute_query_fetchall,
    single_value_sql
)
logger = logging.getLogger("webapi")


def add_param_to_dict(dictionary, key, value):
    """
    Dispatch a list of parameters into a dictionary.
    """
    for i, elem in enumerate(value):
        dictionary[key + str(i)] = elem
    return dictionary


class PostgreSQLBase(object):

    """
    Base class for PostgreSQL based service implementations.
    """

    def __init__(self, *args, **kwargs):
        """
        Store the config and create a connection to the database.

        Keyword arguments:
        config -- Configuration of the application.

        """
        self.context = kwargs.get("config")
        try:
            self.database = self.context.database_class(
                self.context
            )
        except KeyError:
            # some tests seem to put the database config parameters
            # into a namespace called 'database', others do not
            self.database = self.context.database.database_class(
                self.context.database
            )

    @contextlib.contextmanager
    def get_connection(self):
        connection = self.database.connection()
        try:
            yield connection
        finally:
            connection.close()

    def query(self, sql, params=None, error_message=None, connection=None):
        """Return the result of a query executed against PostgreSQL.

        Create a connection, open a cursor, execute the query and return the
        results. If an error occures, log it and raise a DatabaseError.

        Keyword arguments:
        sql -- SQL query to execute.
        params -- Parameters to merge into the SQL query when executed.
        error_message -- Eventual error message to log.
        connection -- Optional connection to the database. If none, a new one
                      will be opened.

        """
        return self._execute(
            execute_query_fetchall,
            sql,
            error_message or "Failed to execute query against PostgreSQL",
            params=params,
            connection=connection
        )

    def count(self, sql, params=None, error_message=None, connection=None):
        """Return the result of a count SQL query executed against PostgreSQL.

        Create a connection, open a cursor, execute the query and return the
        result. If an error occures, log it and raise a DatabaseError.

        Keyword arguments:
        sql -- SQL query to execute.
        params -- Parameters to merge into the SQL query when executed.
        error_message -- Eventual error message to log.
        connection -- Optional connection to the database. If none, a new one
                      will be opened.

        """
        return self._execute(
            single_value_sql,
            sql,
            error_message or "Failed to execute count against PostgreSQL",
            params=params,
            connection=connection
        )

    def _execute(
        self, actor_function, sql, error_message, params=None, connection=None
    ):
        fresh_connection = False
        try:
            if not connection:
                connection = self.database.connection()
                fresh_connection = True
            # logger.debug(connection.cursor().mogrify(sql, params))
            result = actor_function(connection, sql, params)
            connection.commit()
        except psycopg2.Error, e:
            error_message = "%s - %s" % (error_message, str(e))
            logger.error(error_message, exc_info=True)
            if connection:
                connection.rollback()
            raise DatabaseError(error_message)
        finally:
            if connection and fresh_connection:
                connection.close()
        return result

    @staticmethod
    def parse_versions(versions_list, products):
        """
        Parses the versions, separating by ":" and returning versions
        and products.
        """
        versions = []

        for v in versions_list:
            if v.find(":") > -1:
                pv = v.split(":")
                versions.append(pv[0])
                versions.append(pv[1])
            else:
                products.append(v)

        return (versions, products)

    @staticmethod
    def prepare_terms(terms, search_mode):
        """
        Prepare terms for search, adding '%' where needed,
        given the search mode.
        """
        if search_mode in ("contains", "starts_with"):
            terms = terms.replace("_", "\_").replace("%", "\%")

        if search_mode == "contains":
            terms = "%" + terms + "%"
        elif search_mode == "starts_with":
            terms = terms + "%"
        return terms

    @staticmethod
    def dispatch_params(sql_params, key, value):
        """
        Dispatch a parameter or a list of parameters into the params array.
        """
        if not isinstance(value, list):
            sql_params[key] = value
        else:
            for i, elem in enumerate(value):
                sql_params[key + str(i)] = elem
        return sql_params

    @staticmethod
    def build_reports_sql_from(params):
        """
        Generate and return the FROM part of the final SQL query.
        """
        sql_from = ["FROM reports r"]

        ## Searching through plugins
        if params["report_process"] == "plugin":
            sql_from.append(("plugins_reports ON "
                             "plugins_reports.report_id = r.id"))
            sql_from.append(("plugins ON "
                             "plugins_reports.plugin_id = plugins.id"))

        sql_from = " JOIN ".join(sql_from)
        return sql_from

    @staticmethod
    def build_reports_sql_where(params, sql_params, config):
        """Return a string containing the WHERE part of a search-related SQL
        query.
        """
        if hasattr(config, "webapi"):
            config = config.webapi

        sql_where = ["""
            WHERE r.date_processed BETWEEN %(from_date)s AND %(to_date)s
        """]

        sql_params["from_date"] = params["from_date"]
        sql_params["to_date"] = params["to_date"]

        ## Adding terms to where clause
        if params["terms"]:
            if params["search_mode"] == "is_exactly":
                sql_where.append("r.signature=%(term)s")
            else:
                sql_where.append("r.signature LIKE %(term)s")
            sql_params["term"] = params["terms"]

        ## Adding products to where clause
        if params["products"]:
            products_list = ["r.product=%(product" + str(x) + ")s"
                             for x in range(len(params["products"]))]
            sql_where.append("(%s)" % (" OR ".join(products_list)))
            sql_params = add_param_to_dict(sql_params, "product",
                                           params["products"])

        ## Adding OS to where clause
        if params["os"]:
            os_list = ["r.os_name=%(os" + str(x) + ")s"
                       for x in range(len(params["os"]))]
            sql_where.append("(%s)" % (" OR ".join(os_list)))
            sql_params = add_param_to_dict(sql_params, "os", params["os"])

        ## Adding versions to where clause
        if params["versions"]:
            versions_where = []
            version_index = 0

            # For each version, get information about it
            for i in range(0, len(params["versions"]), 2):
                versions_info = params["versions_info"]
                product = params["versions"][i]
                version = params["versions"][i + 1]

                key = "%s:%s" % (product, version)

                version_data = None
                if key in versions_info:
                    version_data = versions_info[key]

                if version_data and version_data["is_rapid_beta"]:
                    # If the version is a rapid beta, that means it's an
                    # alias for a list of other versions. We thus don't filter
                    # on that version, but on all versions listed in the
                    # version_data that we have.

                    # Get all versions that are linked to this rapid beta.
                    rapid_beta_versions = [
                        x for x in versions_info
                        if versions_info[x]["from_beta_version"] == key
                        and not versions_info[x]["is_rapid_beta"]
                    ]

                    for rapid_beta in rapid_beta_versions:
                        versions_where.append(
                            PostgreSQLBase.build_version_where(
                                product,
                                versions_info[rapid_beta]["version_string"],
                                version_index,
                                sql_params,
                                versions_info[rapid_beta],
                                config
                            )
                        )
                        version_index += 2
                else:
                    # This is a "normal" version, let's filter on it
                    versions_where.append(
                        PostgreSQLBase.build_version_where(
                            product,
                            version,
                            version_index,
                            sql_params,
                            version_data,
                            config
                        )
                    )
                    version_index += 2

                # Bug 1000160. The logic to convert version numbers to what
                # they should actually be has been moved to the processors.
                # However, there will be a period of time when we will have
                # both the "correct" version number and the "wrong" one in our
                # database. We thus need to query for both here.
                versions_where.append(
                    PostgreSQLBase.build_version_where(
                        product,
                        version,
                        version_index,
                        sql_params,
                        None,
                        config
                    )
                )
                version_index += 2

            if versions_where:
                sql_where.append("(%s)" % " OR ".join(versions_where))

        ## Adding build id to where clause
        if params["build_ids"]:
            build_ids_list = ["r.build=%(build" + str(x) + ")s"
                              for x in range(len(params["build_ids"]))]
            sql_where.append("(%s)" % (" OR ".join(build_ids_list)))
            sql_params = add_param_to_dict(sql_params, "build",
                                           params["build_ids"])

        ## Adding reason to where clause
        if params["reasons"]:
            reasons_list = ["r.reason=%(reason" + str(x) + ")s"
                            for x in range(len(params["reasons"]))]
            sql_where.append("(%s)" % (" OR ".join(reasons_list)))
            sql_params = add_param_to_dict(sql_params, "reason",
                                           params["reasons"])

        ## Adding release channels to where clause
        if params["release_channels"]:
            channels_list = [
                "UPPER(r.release_channel)=UPPER(%%(release_channel%s)s)" % x
                for x in range(len(params["release_channels"]))
            ]
            sql_where.append("(%s)" % " OR ".join(channels_list))
            sql_params = add_param_to_dict(
                sql_params,
                "release_channel",
                params["release_channels"]
            )

        ## Adding report type to where clause
        if params["report_type"] == "crash":
            sql_where.append("r.hangid IS NULL")
        elif params["report_type"] == "hang":
            sql_where.append("r.hangid IS NOT NULL")

        ## Searching through plugins
        if params["report_process"] == "plugin":
            sql_where.append("r.process_type = 'plugin'")
            sql_where.append(("plugins_reports.date_processed BETWEEN "
                              "%(from_date)s AND %(to_date)s"))

            if params["plugin_terms"]:
                comp = "="

                if params["plugin_search_mode"] in ("contains", "starts_with"):
                    comp = " LIKE "

                sql_where_plugin_in = []
                for f in params["plugin_in"]:
                    if f == "name":
                        field = "plugins.name"
                    elif f == "filename":
                        field = "plugins.filename"

                    sql_where_plugin_in.append(comp.join((field,
                                                          "%(plugin_term)s")))
                sql_params["plugin_term"] = params["plugin_terms"]

                sql_where.append("(%s)" % " OR ".join(sql_where_plugin_in))

        elif params["report_process"] == "browser":
            sql_where.append("r.process_type IS NULL")

        elif params["report_process"] == "content":
            sql_where.append("r.process_type = 'content'")

        sql_where = " AND ".join(sql_where)
        return (sql_where, sql_params)

    @staticmethod
    def build_reports_sql_limit(params, sql_params):
        """
        """
        sql_limit = """
            LIMIT %(limit)s
            OFFSET %(offset)s
        """
        sql_params["limit"] = params["result_number"]
        sql_params["offset"] = params["result_offset"]

        return (sql_limit, sql_params)

    @staticmethod
    def build_version_where(
        product,
        version,
        version_index,
        sql_params,
        version_data,
        config
    ):
        """Return the content of WHERE of a SQL query for a given version. """
        version_where = []

        product_param = "version%s" % version_index
        version_param = "version%s" % (version_index + 1)

        sql_params[product_param] = product
        sql_params[version_param] = version

        if version_data and version_data["release_channel"]:
            # If we have data about that version, and it has a release channel,
            # we will want to add some more specific filters to the SQL query.

            channel = version_data["release_channel"].lower()

            if channel.startswith(tuple(config.non_release_channels)):
                # This is a non-release channel.

                # Restrict by release_channel.
                version_where.append("r.release_channel ILIKE '%s'" % channel)

                if (
                    channel.startswith(tuple(config.restricted_channels)) and
                    version_data["build_id"]
                ):
                    # Restrict to a list of build_id.
                    builds = ", ".join(
                        "'%s'" % b for b in version_data["build_id"]
                    )
                    version_where.append("r.build IN (%s)" % builds)
            else:
                # It's a release.
                version_where.append((
                    "r.release_channel NOT IN %s" %
                    (tuple(config.non_release_channels),)
                ))

        version_where.append("r.product=%%(version%s)s" % version_index)
        version_where.append("r.version=%%(version%s)s" % (version_index + 1))

        return "(%s)" % " AND ".join(version_where)
