#
# CSS
#

PIPELINE_CSS = {
    'search': {
        'source_filenames': (
            'supersearch/css/search.less',
        ),
        'output_filename': 'css/search.min.css',
    },
    'select2': {
        'source_filenames': (
            'crashstats/js/lib/select2/select2.css',
        ),
        'output_filename': 'css/select2.min.css',
    },
    'jquery_ui': {
        'source_filenames': (
            'crashstats/css/lib/jquery-ui.css',
            'crashstats/css/lib/jquery-ui.structure.css',
            'crashstats/css/lib/jquery-ui.theme.css',
        ),
        'output_filename': 'css/jquery-ui.min.css',
    },
    'accordion': {
        'source_filenames': (
            'crashstats/css/accordion.less',
        ),
        'output_filename': 'css/accordion.min.css',
    },
    'metricsgraphics': {
        'source_filenames': (
            'crashstats/css/lib/metricsgraphics.css',
            'crashstats/css/metricsgraphics_custom.css',
        ),
        'output_filename': 'css/metricsgraphics.min.css',
    },
    'crashstats_base': {
        'source_filenames': (
            'crashstats/css/screen.less',
            'browserid/persona-buttons.css',
        ),
        'output_filename': 'css/crashstats-base.min.css',
    },
    'api_documentation': {
        'source_filenames': (
            'api/css/documentation.css',
        ),
        'output_filename': 'css/api-documentation.min.css',
    },
    'crashes_per_day': {
        'source_filenames': (
            'crashstats/css/crashes_per_day.less',
        ),
        'output_filename': 'css/crashes-per-day.min.css',
    },
    'crontabber_state': {
        'source_filenames': (
            'crashstats/css/crontabber_state.css',
        ),
        'output_filename': 'css/crontabber-state.min.css',
    },
    'daily': {
        'source_filenames': (
            'crashstats/css/daily.less',
        ),
        'output_filename': 'css/daily.min.css',
    },
    'documentation': {
        'source_filenames': (
            'documentation/css/documentation.less',
            'documentation/css/jsonview.custom.less',
        ),
        'output_filename': 'css/documentation.min.css',
    },
    'gccrashes': {
        'source_filenames': (
            'crashstats/css/gccrashes.less',
        ),
        'output_filename': 'css/gccrashes.min.css',
    },
    'report_index': {
        'source_filenames': (
            'crashstats/css/report_index.css',
        ),
        'output_filename': 'css/report-index.min.css',
    },
    'report_list': {
        'source_filenames': (
            'crashstats/css/report_list.less',
        ),
        'output_filename': 'css/report-list.min.css',
    },
    'api_tokens': {
        'source_filenames': (
            'manage/css/api_tokens.css',
        ),
        'output_filename': 'css/api-tokens.min.css',
    },
    'manage:home': {
        'source_filenames': (
            'crashstats/css/lib/font-awesome/css/font-awesome.css',
            'crashstats/css/fonts.less',
            'manage/css/home.less',
        ),
        'output_filename': 'css/manage-home.min.css',
    },
    'manage:supersearch_fields': {
        'source_filenames': (
            'manage/css/supersearch_fields.less',
        ),
        'output_filename': 'css/manage-supersearch-fields.min.css',
    },
    'profile': {
        'source_filenames': (
            'profile/css/profile.css',
        ),
        'output_filename': 'css/profile.min.css',
    },
    'signature_report': {
        'source_filenames': (
            'signature/css/signature_report.less',
        ),
        'output_filename': 'css/signature-report.min.css',
    },
    'symbols': {
        'source_filenames': (
            'symbols/css/home.css',
        ),
        'output_filename': 'css/symbols.min.css',
    },
    'tokens': {
        'source_filenames': (
            'tokens/css/home.css',
        ),
        'output_filename': 'css/tokens.min.css',
    },
    'old_topcrashers': {
        'source_filenames': (
            'crashstats/css/topcrashers.less',
        ),
        'output_filename': 'css/old-topcrashers.min.css',
    },
    'topcrashers': {
        'source_filenames': (
            'topcrashers/css/topcrashers.less',
        ),
        'output_filename': 'css/topcrashers.min.css',
    },

}

#
# JavaScript
#


PIPELINE_JS = {
    'moment': {
        'source_filenames': (
            'crashstats/js/moment.min.js',
        ),
        'output_filename': 'js/moment.min.js',
    },
    'pagination': {
        'source_filenames': (
            'manage/js/pagination_utils.js',
        ),
        'output_filename': 'js/pagination.min.js',
    },
    'dynamic_form': {
        'source_filenames': (
            'supersearch/js/lib/dynamic_form.js',
        ),
        'output_filename': 'js/dynamic-form.min.js',
    },
    'bugzilla': {
        'source_filenames': (
            'crashstats/js/socorro/bugzilla.js',
        ),
        'output_filename': 'js/bugzilla.min.js',
    },
    'd3': {
        'source_filenames': (
            'crashstats/js/lib/d3.min.js',
        ),
        'output_filename': 'js/d3.min.js',
    },
    'jquery_ui': {
        'source_filenames': (
            'crashstats/js/jquery/plugins/jquery-ui.js',
        ),
        'output_filename': 'js/jquery-ui.min.js',
    },
    'accordion': {
        'source_filenames': (
            'crashstats/js/lib/accordions.js',
        ),
        'output_filename': 'js/accordion.min.js',
    },
    'correlation': {
        'source_filenames': (
            'crashstats/js/socorro/correlation.js',
        ),
        'output_filename': 'js/correlation.min.js',
    },
    'metricsgraphics': {
        'source_filenames': (
            'crashstats/js/lib/metricsgraphics.min.js',
        ),
        'output_filename': 'js/metricsgraphics.min.js',
    },
    'select2': {
        'source_filenames': (
            'crashstats/js/lib/select2/select2.js',
        ),
        'output_filename': 'js/select2.min.js',
    },
    'jquery_tablesorter': {
        'source_filenames': (
            'crashstats/js/jquery/plugins/jquery.tablesorter.js',
        ),
        'output_filename': 'js/jquery-tablesorter.min.js',
    },
    'timeutils': {
        'source_filenames': (
            'crashstats/js/timeutils.js',
        ),
        'output_filename': 'js/timeutils.min.js',
    },
    'socorro_utils': {
        'source_filenames': (
            'crashstats/js/socorro/utils.js',
        ),
        'output_filename': 'js/socorro-utils.min.js',
    },
    'topcrash': {
        'source_filenames': (
            'crashstats/js/socorro/topcrash.js',
        ),
        'output_filename': 'js/topcrash.min.js',
    },
    'topcrashers': {
        'source_filenames': (
            'topcrashers/js/topcrashers.js',
        ),
        'output_filename': 'js/topcrashers.min.js',
    },
    'crashstats_base': {
        'source_filenames': (
            'crashstats/js/jquery/jquery-2.0.3.min.js',
            'crashstats/js/jquery/plugins/jquery.cookies.2.2.0.js',
            'crashstats/js/socorro/nav.js',
            'crashstats/js/socorro/analytics.js',
            'browserid/api.js',
            'browserid/browserid.js',
        ),
        'output_filename': 'js/crashstats-base.min.js',
    },
    'api_documentation': {
        'source_filenames': (
            'api/js/lib/filesize.min.js',
            'api/js/testdrive.js'
        ),
        'output_filename': 'js/api-documentation.min.js',
    },
    'crashes_per_day': {
        'source_filenames': (
            'crashstats/js/socorro/crashes_per_day.js',
        ),
        'output_filename': 'js/crashes-per-day.min.js',
    },
    'crontabber_state': {
        'source_filenames': (
            'crashstats/js/underscore-min.js',
            'crashstats/js/lib/sankey.js',
            'crashstats/js/socorro/crontabber_state.js',
        ),
        'output_filename': 'js/crontabber-state.min.js',
    },
    'daily': {  # deprecated
        'source_filenames': (
            'crashstats/js/socorro/daily.js',
        ),
        'output_filename': 'js/daily.min.js',
    },
    'documentation': {
        'source_filenames': (
            'documentation/js/lib/jquery.jsonview.js',
            'documentation/js/documentation.js',
        ),
        'output_filename': 'js/documentation.min.js',
    },
    'exploitability_report': {  # deprecated
        'source_filenames': (
            'crashstats/js/socorro/exploitability_report.js',
        ),
        'output_filename': 'js/exploitability-report.min.js',
    },
    'exploitability': {
        'source_filenames': (
            'crashstats/js/socorro/exploitability.js',
        ),
        'output_filename': 'js/exploitability.min.js',
    },
    'gccrashes': {
        'source_filenames': (
            'crashstats/js/socorro/gccrashes.js',
        ),
        'output_filename': 'js/gccrashes.min.js',
    },
    'daily': {
        'source_filenames': (
            'crashstats/js/socorro/daily.js',
        ),
        'output_filename': 'js/daily.min.js',
    },
    'home': {
        'source_filenames': (
            'home/js/home.js',
        ),
        'output_filename': 'js/home.min.js',
    },
    'report_index': {
        'source_filenames': (
            'crashstats/js/socorro/report.js',
        ),
        'output_filename': 'js/report-index.min.js',
    },
    'report_list': {
        'source_filenames': (
            'crashstats/js/jquery/plugins/jquery.cookie.js',
            'crashstats/js/lib/awty.js',
            'crashstats/js/socorro/report_list.js',
            'crashstats/js/socorro/report_list_signature_summary.js',
            'crashstats/js/socorro/report_list_graph.js',
            'crashstats/js/socorro/report_list_reports.js',
            'crashstats/js/socorro/report_list_comments.js',
            'crashstats/js/socorro/report_list_correlations.js',
            'crashstats/js/socorro/report_list_sigurls.js',
            'crashstats/js/socorro/report_list_bugzilla.js',
            'crashstats/js/socorro/report_list_table.js',
        ),
        'output_filename': 'js/report-list.min.js',
    },
    'status': {
        'source_filenames': (
            'crashstats/js/lib/filesize.min.js',
            'crashstats/js/flot-0.7/jquery.flot.pack.js',
            'crashstats/js/timeago/jquery.timeago.js',
            'crashstats/js/socorro/server_status.js',
        ),
        'output_filename': 'js/status.min.js',
    },
    'api_tokens': {
        'source_filenames': (
            'manage/js/api_tokens.js',
        ),
        'output_filename': 'js/api-tokens.min.js',
    },
    'manage:events': {
        'source_filenames': (
            'manage/js/events.js',
        ),
        'output_filename': 'js/manage-events.min.js',
    },
    'manage:featured_versions': {
        'source_filenames': (
            'manage/js/featured-versions.js',
        ),
        'output_filename': 'js/manage-featured-versions.min.js',
    },
    'manage:fields': {
        'source_filenames': (
            'manage/js/fields.js',
        ),
        'output_filename': 'js/manage-fields.min.js',
    },
    'manage:graphics_devices': {
        'source_filenames': (
            'manage/js/graphics_devices.js',
        ),
        'output_filename': 'js/manage-graphics-devices.min.js',
    },
    'manage:groups': {
        'source_filenames': (
            'manage/js/groups.js',
        ),
        'output_filename': 'js/manage-groups.min.js',
    },
    'manage:skiplist': {
        'source_filenames': (
            'manage/js/skiplist.js',
        ),
        'output_filename': 'js/manage-skiplist.min.js',
    },
    'manage:supersearch_field': {
        'source_filenames': (
            'manage/js/supersearch_field.js',
        ),
        'output_filename': 'js/manage-supersearch-field.min.js',
    },
    'manage:supersearch_fields': {
        'source_filenames': (
            'manage/js/supersearch_fields.js',
        ),
        'output_filename': 'js/manage-supersearch-fields.min.js',
    },
    'manage:symbols_uploads': {
        'source_filenames': (
            'manage/js/symbols-uploads.js',
        ),
        'output_filename': 'js/manage-symbols-uploads.min.js',
    },
    'manage:users': {
        'source_filenames': (
            'manage/js/users.js',
        ),
        'output_filename': 'js/manage-users.min.js',
    },
    'profile': {
        'source_filenames': (
            'profile/js/profile.js',
        ),
        'output_filename': 'js/profile.min.js',
    },
    'signature_report': {
        'source_filenames': (
            'signature/js/signature_report.js',
            'signature/js/signature_tab.js',
            'signature/js/signature_tab_summary.js',
            'signature/js/signature_tab_graphs.js',
            'signature/js/signature_tab_reports.js',
            'signature/js/signature_tab_aggregations.js',
            'signature/js/signature_tab_comments.js',
            'signature/js/signature_tab_correlations.js',
            'signature/js/signature_tab_bugzilla.js',
            'signature/js/signature_tab_graph.js',
            'signature/js/signature_panel.js',
        ),
        'output_filename': 'js/signature-report.min.js',
    },
    'search_custom': {
        'source_filenames': (
            'supersearch/js/lib/ace/ace.js',
            'supersearch/js/lib/ace/theme-monokai.js',
            'supersearch/js/lib/ace/mode-json.js',
            'supersearch/js/socorro/search_custom.js',
        ),
        'output_filename': 'js/search-custom.min.js',
    },
    'search': {
        'source_filenames': (
            'supersearch/js/socorro/search.js',
        ),
        'output_filename': 'js/search.min.js',
    },
    'tokens': {
        'source_filenames': (
            'tokens/js/home.js',
        ),
        'output_filename': 'js/tokens.min.js',
    },
}

# This is sanity checks, primarily for developers. It checks that
# you haven't haven't accidentally make a string a tuple with an
# excess comma, no underscores in the bundle name and that the
# bundle file extension is either .js or .css.
# We also check, but only warn, if a file is re-used in a different bundle.
# That's because you might want to consider not including that file in the
# bundle and instead break it out so it can be re-used on its own.
_used = {}
for config in PIPELINE_JS, PIPELINE_CSS:  # NOQA
    _trouble = set()
    for k, v in config.items():
        assert isinstance(k, basestring), k
        out = v['output_filename']
        assert isinstance(v['source_filenames'], tuple), v
        assert isinstance(out, basestring), v
        assert not out.split('/')[-1].startswith('.'), k
        assert '_' not in out
        assert out.endswith('.min.css') or out.endswith('.min.js')
        for asset_file in v['source_filenames']:
            if asset_file in _used:
                # Consider using warnings.warn here instead
                print '{:<52} in {:<20} already in {}'.format(
                    asset_file,
                    k,
                    _used[asset_file]
                )
                _trouble.add(asset_file)
            _used[asset_file] = k

    for asset_file in _trouble:
        print "REPEATED", asset_file
        found_in = []
        sets = []
        for k, v in config.items():
            if asset_file in v['source_filenames']:
                found_in.append(k)
                sets.append(set(list(v['source_filenames'])))
        print "FOUND IN", found_in
        print "ALWAYS TOGETHER WITH", set.intersection(*sets)
        break
