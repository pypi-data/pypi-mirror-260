from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/router-bgp.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_bgp = resolve('router_bgp')
    l_0_distance_cli = resolve('distance_cli')
    l_0_paths_cli = resolve('paths_cli')
    l_0_rr_preserve_attributes_cli = resolve('rr_preserve_attributes_cli')
    l_0_namespace = resolve('namespace')
    l_0_temp = resolve('temp')
    l_0_neighbor_interfaces = resolve('neighbor_interfaces')
    l_0_rib_position = resolve('rib_position')
    l_0_row_default_encapsulation = resolve('row_default_encapsulation')
    l_0_row_nhs_source_interface = resolve('row_nhs_source_interface')
    l_0_evpn_hostflap_detection_window = resolve('evpn_hostflap_detection_window')
    l_0_evpn_hostflap_detection_threshold = resolve('evpn_hostflap_detection_threshold')
    l_0_evpn_hostflap_detection_expiry = resolve('evpn_hostflap_detection_expiry')
    l_0_evpn_hostflap_detection_state = resolve('evpn_hostflap_detection_state')
    l_0_evpn_gw_config = resolve('evpn_gw_config')
    l_0_path_selection_roles = resolve('path_selection_roles')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.filters['first']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'first' found.")
    try:
        t_4 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_5 = environment.filters['length']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'length' found.")
    try:
        t_6 = environment.filters['list']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No filter named 'list' found.")
    try:
        t_7 = environment.filters['map']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No filter named 'map' found.")
    try:
        t_8 = environment.filters['selectattr']
    except KeyError:
        @internalcode
        def t_8(*unused):
            raise TemplateRuntimeError("No filter named 'selectattr' found.")
    try:
        t_9 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_9(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_9((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp)):
        pass
        yield '\n### Router BGP\n\nASN Notation: '
        yield str(t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as_notation'), 'asplain'))
        yield '\n\n#### Router BGP Summary\n\n| BGP AS | Router ID |\n| ------ | --------- |\n| '
        yield str(t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as'), '-'))
        yield ' | '
        yield str(t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'router_id'), '-'))
        yield ' |\n'
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id')):
            pass
            yield '\n| BGP AS | Cluster ID |\n| ------ | --------- |\n| '
            yield str(t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as'), '-'))
            yield ' | '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id'))
            yield ' |\n'
        if (t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_defaults')) or t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'))):
            pass
            yield '\n| BGP Tuning |\n| ---------- |\n'
            for l_1_bgp_default in t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_defaults'), []):
                _loop_vars = {}
                pass
                yield '| '
                yield str(l_1_bgp_default)
                yield ' |\n'
            l_1_bgp_default = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'enabled'), True):
                pass
                if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time')):
                    pass
                    yield '| graceful-restart restart-time '
                    yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time'))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time')):
                    pass
                    yield '| graceful-restart stalepath-time '
                    yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time'))
                    yield ' |\n'
                yield '| graceful-restart |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), False):
                pass
                yield '| no graceful-restart-helper |\n'
            elif t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), True):
                pass
                if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time')):
                    pass
                    yield '| graceful-restart-helper restart-time '
                    yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time'))
                    yield ' |\n'
                elif t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'long_lived'), True):
                    pass
                    yield '| graceful-restart-helper long-lived |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'bestpath'), 'd_path'), True):
                pass
                yield '| bgp bestpath d-path |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_for_convergence'), True):
                pass
                yield '| update wait-for-convergence |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_install'), True):
                pass
                yield '| update wait-install |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), True):
                pass
                yield '| bgp default ipv4-unicast |\n'
            elif t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), False):
                pass
                yield '| no bgp default ipv4-unicast |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), True):
                pass
                yield '| bgp default ipv4-unicast transport ipv6 |\n'
            elif t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), False):
                pass
                yield '| no bgp default ipv4-unicast transport ipv6 |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes')):
                pass
                l_0_distance_cli = str_join(('distance bgp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes'), ))
                context.vars['distance_cli'] = l_0_distance_cli
                context.exported_vars.add('distance_cli')
                if (t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes')) and t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'))):
                    pass
                    l_0_distance_cli = str_join(((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes'), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'), ))
                    context.vars['distance_cli'] = l_0_distance_cli
                    context.exported_vars.add('distance_cli')
                yield '| '
                yield str((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli))
                yield ' |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths')):
                pass
                l_0_paths_cli = str_join(('maximum-paths ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths'), ))
                context.vars['paths_cli'] = l_0_paths_cli
                context.exported_vars.add('paths_cli')
                if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp')):
                    pass
                    l_0_paths_cli = str_join(((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli), ' ecmp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp'), ))
                    context.vars['paths_cli'] = l_0_paths_cli
                    context.exported_vars.add('paths_cli')
                yield '| '
                yield str((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli))
                yield ' |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'enabled'), True):
                pass
                l_0_rr_preserve_attributes_cli = 'bgp route-reflector preserve-attributes'
                context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
                context.exported_vars.add('rr_preserve_attributes_cli')
                if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'always'), True):
                    pass
                    l_0_rr_preserve_attributes_cli = str_join(((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli), ' always', ))
                    context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
                    context.exported_vars.add('rr_preserve_attributes_cli')
                yield '| '
                yield str((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli))
                yield ' |\n'
        l_0_temp = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['temp'] = l_0_temp
        context.exported_vars.add('temp')
        if not isinstance(l_0_temp, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_temp['bgp_vrf_listen_ranges'] = False
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs')):
            pass
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_vrf, 'listen_ranges')):
                    pass
                    if not isinstance(l_0_temp, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_0_temp['bgp_vrf_listen_ranges'] = True
                    break
            l_1_vrf = missing
        if (t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges')) or t_9(environment.getattr((undefined(name='temp') if l_0_temp is missing else l_0_temp), 'bgp_vrf_listen_ranges'), True)):
            pass
            yield '\n#### Router BGP Listen Ranges\n\n| Prefix | Peer-ID Include Router ID | Peer Group | Peer-Filter | Remote-AS | VRF |\n| ------ | ------------------------- | ---------- | ----------- | --------- | --- |\n'
            if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges')):
                pass
                def t_10(fiter):
                    for l_1_listen_range in fiter:
                        if ((t_9(environment.getattr(l_1_listen_range, 'peer_group')) and t_9(environment.getattr(l_1_listen_range, 'prefix'))) and (t_9(environment.getattr(l_1_listen_range, 'peer_filter')) or t_9(environment.getattr(l_1_listen_range, 'remote_as')))):
                            yield l_1_listen_range
                for l_1_listen_range in t_10(t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges'), 'peer_group')):
                    l_1_row_remote_as = resolve('row_remote_as')
                    _loop_vars = {}
                    pass
                    if t_9(environment.getattr(l_1_listen_range, 'peer_filter')):
                        pass
                        l_1_row_remote_as = '-'
                        _loop_vars['row_remote_as'] = l_1_row_remote_as
                    elif t_9(environment.getattr(l_1_listen_range, 'remote_as')):
                        pass
                        l_1_row_remote_as = environment.getattr(l_1_listen_range, 'remote_as')
                        _loop_vars['row_remote_as'] = l_1_row_remote_as
                    yield '| '
                    yield str(environment.getattr(l_1_listen_range, 'prefix'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_listen_range, 'peer_id_include_router_id'), '-'))
                    yield ' | '
                    yield str(environment.getattr(l_1_listen_range, 'peer_group'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_listen_range, 'peer_filter'), '-'))
                    yield ' | '
                    yield str((undefined(name='row_remote_as') if l_1_row_remote_as is missing else l_1_row_remote_as))
                    yield ' | default |\n'
                l_1_listen_range = l_1_row_remote_as = missing
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_vrf, 'listen_ranges')):
                    pass
                    def t_11(fiter):
                        for l_2_listen_range in fiter:
                            if ((t_9(environment.getattr(l_2_listen_range, 'peer_group')) and t_9(environment.getattr(l_2_listen_range, 'prefix'))) and (t_9(environment.getattr(l_2_listen_range, 'peer_filter')) or t_9(environment.getattr(l_2_listen_range, 'remote_as')))):
                                yield l_2_listen_range
                    for l_2_listen_range in t_11(t_2(environment.getattr(l_1_vrf, 'listen_ranges'), 'peer_group')):
                        l_2_row_remote_as = resolve('row_remote_as')
                        _loop_vars = {}
                        pass
                        if t_9(environment.getattr(l_2_listen_range, 'peer_filter')):
                            pass
                            l_2_row_remote_as = '-'
                            _loop_vars['row_remote_as'] = l_2_row_remote_as
                        elif t_9(environment.getattr(l_2_listen_range, 'remote_as')):
                            pass
                            l_2_row_remote_as = environment.getattr(l_2_listen_range, 'remote_as')
                            _loop_vars['row_remote_as'] = l_2_row_remote_as
                        yield '| '
                        yield str(environment.getattr(l_2_listen_range, 'prefix'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_listen_range, 'peer_id_include_router_id'), '-'))
                        yield ' | '
                        yield str(environment.getattr(l_2_listen_range, 'peer_group'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_listen_range, 'peer_filter'), '-'))
                        yield ' | '
                        yield str((undefined(name='row_remote_as') if l_2_row_remote_as is missing else l_2_row_remote_as))
                        yield ' | '
                        yield str(environment.getattr(l_1_vrf, 'name'))
                        yield ' |\n'
                    l_2_listen_range = l_2_row_remote_as = missing
            l_1_vrf = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups')):
            pass
            yield '\n#### Router BGP Peer Groups\n'
            for l_1_peer_group in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), 'name'):
                l_1_remove_private_as_setting = resolve('remove_private_as_setting')
                l_1_remove_private_as_ingress_setting = resolve('remove_private_as_ingress_setting')
                l_1_neighbor_rib_in_pre_policy_retain_row = resolve('neighbor_rib_in_pre_policy_retain_row')
                l_1_timers = resolve('timers')
                l_1_value = resolve('value')
                _loop_vars = {}
                pass
                yield '\n##### '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield '\n\n| Settings | Value |\n| -------- | ----- |\n'
                if t_9(environment.getattr(l_1_peer_group, 'type')):
                    pass
                    yield '| Address Family | '
                    yield str(environment.getattr(l_1_peer_group, 'type'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'shutdown'), True):
                    pass
                    yield '| Shutdown | '
                    yield str(environment.getattr(l_1_peer_group, 'shutdown'))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled')):
                    pass
                    l_1_remove_private_as_setting = environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled')
                    _loop_vars['remove_private_as_setting'] = l_1_remove_private_as_setting
                    if ((environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled') == True) and t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'all'), True)):
                        pass
                        l_1_remove_private_as_setting = str_join(((undefined(name='remove_private_as_setting') if l_1_remove_private_as_setting is missing else l_1_remove_private_as_setting), ' (All)', ))
                        _loop_vars['remove_private_as_setting'] = l_1_remove_private_as_setting
                        if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'replace_as'), True):
                            pass
                            l_1_remove_private_as_setting = str_join(((undefined(name='remove_private_as_setting') if l_1_remove_private_as_setting is missing else l_1_remove_private_as_setting), ' (Replace AS)', ))
                            _loop_vars['remove_private_as_setting'] = l_1_remove_private_as_setting
                    yield '| Remove Private AS Outbound | '
                    yield str((undefined(name='remove_private_as_setting') if l_1_remove_private_as_setting is missing else l_1_remove_private_as_setting))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled')):
                    pass
                    l_1_remove_private_as_ingress_setting = environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled')
                    _loop_vars['remove_private_as_ingress_setting'] = l_1_remove_private_as_ingress_setting
                    if ((environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled') == True) and t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'replace_as'), True)):
                        pass
                        l_1_remove_private_as_ingress_setting = str_join(((undefined(name='remove_private_as_ingress_setting') if l_1_remove_private_as_ingress_setting is missing else l_1_remove_private_as_ingress_setting), ' (Replace AS)', ))
                        _loop_vars['remove_private_as_ingress_setting'] = l_1_remove_private_as_ingress_setting
                    yield '| Remove Private AS Inbound | '
                    yield str((undefined(name='remove_private_as_ingress_setting') if l_1_remove_private_as_ingress_setting is missing else l_1_remove_private_as_ingress_setting))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'enabled'), True):
                    pass
                    yield '| Allowas-in | Allowed, allowed '
                    yield str(t_1(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'times'), '3 (default)'))
                    yield ' times |\n'
                if t_9(environment.getattr(l_1_peer_group, 'remote_as')):
                    pass
                    yield '| Remote AS | '
                    yield str(environment.getattr(l_1_peer_group, 'remote_as'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'local_as')):
                    pass
                    yield '| Local AS | '
                    yield str(environment.getattr(l_1_peer_group, 'local_as'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'route_reflector_client')):
                    pass
                    yield '| Route Reflector Client | Yes |\n'
                if t_9(environment.getattr(l_1_peer_group, 'bgp_listen_range_prefix')):
                    pass
                    yield '| Listen range prefix | '
                    yield str(environment.getattr(l_1_peer_group, 'bgp_listen_range_prefix'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'next_hop_self'), True):
                    pass
                    yield '| Next-hop self | True |\n'
                if t_9(environment.getattr(l_1_peer_group, 'next_hop_unchanged'), True):
                    pass
                    yield '| Next-hop unchanged | True |\n'
                if t_9(environment.getattr(l_1_peer_group, 'update_source')):
                    pass
                    yield '| Source | '
                    yield str(environment.getattr(l_1_peer_group, 'update_source'))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled')):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain_row = environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled')
                    _loop_vars['neighbor_rib_in_pre_policy_retain_row'] = l_1_neighbor_rib_in_pre_policy_retain_row
                    if (t_9(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled'), True) and t_9(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'all'), True)):
                        pass
                        l_1_neighbor_rib_in_pre_policy_retain_row = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_row') if l_1_neighbor_rib_in_pre_policy_retain_row is missing else l_1_neighbor_rib_in_pre_policy_retain_row), ' (All)', ))
                        _loop_vars['neighbor_rib_in_pre_policy_retain_row'] = l_1_neighbor_rib_in_pre_policy_retain_row
                    yield '| RIB Pre-Policy Retain | '
                    yield str((undefined(name='neighbor_rib_in_pre_policy_retain_row') if l_1_neighbor_rib_in_pre_policy_retain_row is missing else l_1_neighbor_rib_in_pre_policy_retain_row))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'bfd'), True):
                    pass
                    yield '| BFD | True |\n'
                if ((t_9(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'interval')) and t_9(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'min_rx'))) and t_9(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'multiplier'))):
                    pass
                    l_1_timers = str_join(('interval: ', environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'interval'), ', min_rx: ', environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'min_rx'), ', multiplier: ', environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'multiplier'), ))
                    _loop_vars['timers'] = l_1_timers
                    yield '| BFD Timers | '
                    yield str((undefined(name='timers') if l_1_timers is missing else l_1_timers))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'ebgp_multihop')):
                    pass
                    yield '| Ebgp multihop | '
                    yield str(environment.getattr(l_1_peer_group, 'ebgp_multihop'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'ttl_maximum_hops')):
                    pass
                    yield '| TTL Max Hops | '
                    yield str(environment.getattr(l_1_peer_group, 'ttl_maximum_hops'))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'enabled'), True):
                    pass
                    yield '| Default originate | True |\n'
                if t_9(environment.getattr(l_1_peer_group, 'session_tracker')):
                    pass
                    yield '| Session tracker | '
                    yield str(environment.getattr(l_1_peer_group, 'session_tracker'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'send_community')):
                    pass
                    yield '| Send community | '
                    yield str(environment.getattr(l_1_peer_group, 'send_community'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'maximum_routes')):
                    pass
                    if (environment.getattr(l_1_peer_group, 'maximum_routes') == 0):
                        pass
                        l_1_value = '0 (no limit)'
                        _loop_vars['value'] = l_1_value
                    else:
                        pass
                        l_1_value = environment.getattr(l_1_peer_group, 'maximum_routes')
                        _loop_vars['value'] = l_1_value
                    if (t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit')) or t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_only'), True)):
                        pass
                        l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ' (', ))
                        _loop_vars['value'] = l_1_value
                        if t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit')):
                            pass
                            l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), 'warning-limit ', environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit'), ))
                            _loop_vars['value'] = l_1_value
                            if t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_only'), True):
                                pass
                                l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ', ', ))
                                _loop_vars['value'] = l_1_value
                            else:
                                pass
                                l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ')', ))
                                _loop_vars['value'] = l_1_value
                        if t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_only'), True):
                            pass
                            l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), 'warning-only)', ))
                            _loop_vars['value'] = l_1_value
                    yield '| Maximum routes | '
                    yield str((undefined(name='value') if l_1_value is missing else l_1_value))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'enabled'), True):
                    pass
                    l_1_value = 'enabled'
                    _loop_vars['value'] = l_1_value
                    if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default')):
                        pass
                        l_1_value = str_join(('default ', environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default'), ))
                        _loop_vars['value'] = l_1_value
                    yield '| Link-Bandwidth | '
                    yield str((undefined(name='value') if l_1_value is missing else l_1_value))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'passive'), True):
                    pass
                    yield '| Passive | True |\n'
            l_1_peer_group = l_1_remove_private_as_setting = l_1_remove_private_as_ingress_setting = l_1_neighbor_rib_in_pre_policy_retain_row = l_1_timers = l_1_value = missing
        l_0_temp = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['temp'] = l_0_temp
        context.exported_vars.add('temp')
        if not isinstance(l_0_temp, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_temp['bgp_vrf_neighbors'] = False
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs')):
            pass
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_vrf, 'neighbors')):
                    pass
                    if not isinstance(l_0_temp, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_0_temp['bgp_vrf_neighbors'] = True
                    break
            l_1_vrf = missing
        if (t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbors')) or t_9(environment.getattr((undefined(name='temp') if l_0_temp is missing else l_0_temp), 'bgp_vrf_neighbors'), True)):
            pass
            yield '\n#### BGP Neighbors\n\n| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |\n| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |\n'
            for l_1_neighbor in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbors'), 'ip_address'):
                l_1_inherited = resolve('inherited')
                l_1_neighbor_peer_group = resolve('neighbor_peer_group')
                l_1_peer_group = resolve('peer_group')
                l_1_neighbor_rib_in_pre_policy_retain = resolve('neighbor_rib_in_pre_policy_retain')
                l_1_value = resolve('value')
                l_1_value_allowas = resolve('value_allowas')
                l_1_active_parameter = l_1_ttl_maximum_hops = missing
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_neighbor, 'peer_group')):
                    pass
                    l_1_inherited = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                    _loop_vars['inherited'] = l_1_inherited
                    l_1_neighbor_peer_group = environment.getattr(l_1_neighbor, 'peer_group')
                    _loop_vars['neighbor_peer_group'] = l_1_neighbor_peer_group
                    l_1_peer_group = t_3(environment, t_8(context, t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), []), 'name', 'arista.avd.defined', (undefined(name='neighbor_peer_group') if l_1_neighbor_peer_group is missing else l_1_neighbor_peer_group)))
                    _loop_vars['peer_group'] = l_1_peer_group
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'remote_as')):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['remote_as'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'vrf')):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['vrf'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'send_community')):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['send_community'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'maximum_routes')):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['maximum_routes'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'allowas_in'), 'enabled'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['allowas_in'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'bfd'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['bfd'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                        if ((t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'bfd_timers'), 'interval')) and t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'bfd_timers'), 'min_rx'))) and t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'bfd_timers'), 'multiplier'))):
                            pass
                            if not isinstance(l_1_inherited, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_1_inherited['bfd_timers'] = str_join(('interval: ', environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'bfd_timers'), 'interval'), ', min_rx: ', environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'bfd_timers'), 'min_rx'), ', multiplier: ', environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'bfd_timers'), 'multiplier'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'shutdown'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['shutdown'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'rib_in_pre_policy_retain'), 'enabled'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['rib_in_pre_policy_retain'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'route_reflector_client'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['route_reflector_client'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'passive'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['passive'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'ttl_maximum_hops')):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['ttl_maximum_hops'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                l_1_active_parameter = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                _loop_vars['active_parameter'] = l_1_active_parameter
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['remote_as'] = t_1(environment.getattr(l_1_neighbor, 'remote_as'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'remote_as'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['vrf'] = t_1(environment.getattr(l_1_neighbor, 'vrf'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'vrf'), 'default')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['send_community'] = t_1(environment.getattr(l_1_neighbor, 'send_community'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'send_community'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['bfd'] = t_1(environment.getattr(l_1_neighbor, 'bfd'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'bfd'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['bfd_timers'] = t_1(environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'bfd_timers'), '-')
                if ((t_9(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'interval')) and t_9(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'min_rx'))) and t_9(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'multiplier'))):
                    pass
                    if not isinstance(l_1_active_parameter, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_1_active_parameter['bfd_timers'] = str_join(('interval: ', environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'interval'), ', min_rx: ', environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'min_rx'), ', multiplier: ', environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'multiplier'), ))
                if ((environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'bfd') != '-') and (environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'bfd_timers') != '-')):
                    pass
                    if not isinstance(l_1_active_parameter, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_1_active_parameter['bfd'] = str_join((environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'bfd'), '(', environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'bfd_timers'), ')', ))
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['shutdown'] = t_1(environment.getattr(l_1_neighbor, 'shutdown'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'shutdown'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['route_reflector_client'] = t_1(environment.getattr(l_1_neighbor, 'route_reflector_client'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'route_reflector_client'), '-')
                if t_9(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled')):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain = environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled')
                    _loop_vars['neighbor_rib_in_pre_policy_retain'] = l_1_neighbor_rib_in_pre_policy_retain
                    if (t_9(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True) and t_9(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'all'), True)):
                        pass
                        l_1_neighbor_rib_in_pre_policy_retain = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain') if l_1_neighbor_rib_in_pre_policy_retain is missing else l_1_neighbor_rib_in_pre_policy_retain), ' (All)', ))
                        _loop_vars['neighbor_rib_in_pre_policy_retain'] = l_1_neighbor_rib_in_pre_policy_retain
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['rib_in_pre_policy_retain'] = t_1((undefined(name='neighbor_rib_in_pre_policy_retain') if l_1_neighbor_rib_in_pre_policy_retain is missing else l_1_neighbor_rib_in_pre_policy_retain), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'rib_in_pre_policy_retain'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['passive'] = t_1(environment.getattr(l_1_neighbor, 'passive'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'passive'), '-')
                if t_9(environment.getattr(l_1_neighbor, 'maximum_routes')):
                    pass
                    if (environment.getattr(l_1_neighbor, 'maximum_routes') == 0):
                        pass
                        l_1_value = '0 (no limit)'
                        _loop_vars['value'] = l_1_value
                    else:
                        pass
                        l_1_value = environment.getattr(l_1_neighbor, 'maximum_routes')
                        _loop_vars['value'] = l_1_value
                    if (t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit')) or t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_only'), True)):
                        pass
                        l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ' (', ))
                        _loop_vars['value'] = l_1_value
                        if t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit')):
                            pass
                            l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), 'warning-limit ', environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit'), ))
                            _loop_vars['value'] = l_1_value
                            if t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_only'), True):
                                pass
                                l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ', ', ))
                                _loop_vars['value'] = l_1_value
                            else:
                                pass
                                l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ')', ))
                                _loop_vars['value'] = l_1_value
                        if t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_only'), True):
                            pass
                            l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), 'warning-only)', ))
                            _loop_vars['value'] = l_1_value
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['maximum_routes'] = t_1((undefined(name='value') if l_1_value is missing else l_1_value), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'maximum_routes'), '-')
                if t_9(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'enabled'), True):
                    pass
                    if t_9(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times')):
                        pass
                        l_1_value_allowas = str_join(('Allowed, allowed ', environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times'), ' times', ))
                        _loop_vars['value_allowas'] = l_1_value_allowas
                    else:
                        pass
                        l_1_value_allowas = 'Allowed, allowed 3 (default) times'
                        _loop_vars['value_allowas'] = l_1_value_allowas
                l_1_ttl_maximum_hops = t_1(environment.getattr(l_1_neighbor, 'ttl_maximum_hops'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'ttl_maximum_hops'), '-')
                _loop_vars['ttl_maximum_hops'] = l_1_ttl_maximum_hops
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['allowas_in'] = t_1((undefined(name='value_allowas') if l_1_value_allowas is missing else l_1_value_allowas), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'allowas_in'), '-')
                yield '| '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'remote_as'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'vrf'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'shutdown'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'send_community'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'maximum_routes'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'allowas_in'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'bfd'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'rib_in_pre_policy_retain'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'route_reflector_client'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'passive'))
                yield ' | '
                yield str((undefined(name='ttl_maximum_hops') if l_1_ttl_maximum_hops is missing else l_1_ttl_maximum_hops))
                yield ' |\n'
            l_1_neighbor = l_1_inherited = l_1_neighbor_peer_group = l_1_peer_group = l_1_active_parameter = l_1_neighbor_rib_in_pre_policy_retain = l_1_value = l_1_value_allowas = l_1_ttl_maximum_hops = missing
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_vrf, 'neighbors')):
                    pass
                    for l_2_neighbor in environment.getattr(l_1_vrf, 'neighbors'):
                        l_2_neighbor_peer_group = resolve('neighbor_peer_group')
                        l_2_peer_group = resolve('peer_group')
                        l_2_value = resolve('value')
                        l_2_value_allowas = resolve('value_allowas')
                        l_2_neighbor_rib_in_pre_policy_retain = resolve('neighbor_rib_in_pre_policy_retain')
                        l_2_inherited_vrf = l_2_active_parameter_vrf = missing
                        _loop_vars = {}
                        pass
                        l_2_inherited_vrf = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                        _loop_vars['inherited_vrf'] = l_2_inherited_vrf
                        if t_9(environment.getattr(l_2_neighbor, 'peer_group')):
                            pass
                            l_2_neighbor_peer_group = environment.getattr(l_2_neighbor, 'peer_group')
                            _loop_vars['neighbor_peer_group'] = l_2_neighbor_peer_group
                            l_2_peer_group = t_3(environment, t_8(context, t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), []), 'name', 'arista.avd.defined', (undefined(name='neighbor_peer_group') if l_2_neighbor_peer_group is missing else l_2_neighbor_peer_group)))
                            _loop_vars['peer_group'] = l_2_peer_group
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'remote_as')):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['remote_as'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'send_community')):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['send_community'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'maximum_routes')):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['maximum_routes'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'allowas_in'), 'enabled'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['allowas_in'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'bfd'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['bfd'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                                if ((t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'bfd_timers'), 'interval')) and t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'bfd_timers'), 'min_rx'))) and t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'bfd_timers'), 'multiplier'))):
                                    pass
                                    if not isinstance(l_2_inherited_vrf, Namespace):
                                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                    l_2_inherited_vrf['bfd_timers'] = str_join(('interval: ', environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'bfd_timers'), 'interval'), ', min_rx: ', environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'bfd_timers'), 'min_rx'), ', multiplier: ', environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'bfd_timers'), 'multiplier'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'shutdown'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['shutdown'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'rib_in_pre_policy_retain'), 'enabled'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['rib_in_pre_policy_retain'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'route_reflector_client'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['route_reflector_client'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'passive'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['passive'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                        l_2_active_parameter_vrf = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                        _loop_vars['active_parameter_vrf'] = l_2_active_parameter_vrf
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['remote_as'] = t_1(environment.getattr(l_2_neighbor, 'remote_as'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'remote_as'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['send_community'] = t_1(environment.getattr(l_2_neighbor, 'send_community'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'send_community'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['bfd'] = t_1(environment.getattr(l_2_neighbor, 'bfd'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'bfd'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['bfd_timers'] = t_1(environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'bfd_timers'), '-')
                        if ((t_9(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'interval')) and t_9(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'min_rx'))) and t_9(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'multiplier'))):
                            pass
                            if not isinstance(l_2_active_parameter_vrf, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_active_parameter_vrf['bfd_timers'] = str_join(('interval: ', environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'interval'), ', min_rx: ', environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'min_rx'), ', multiplier: ', environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'multiplier'), ))
                        if ((environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'bfd') != '-') and (environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'bfd_timers') != '-')):
                            pass
                            if not isinstance(l_2_active_parameter_vrf, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_active_parameter_vrf['bfd'] = str_join((environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'bfd'), '(', environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'bfd_timers'), ')', ))
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['shutdown'] = t_1(environment.getattr(l_2_neighbor, 'shutdown'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'shutdown'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['route_reflector_client'] = t_1(environment.getattr(l_2_neighbor, 'route_reflector_client'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'route_reflector_client'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['passive'] = t_1(environment.getattr(l_2_neighbor, 'passive'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'passive'), '-')
                        if t_9(environment.getattr(l_2_neighbor, 'maximum_routes')):
                            pass
                            if (environment.getattr(l_2_neighbor, 'maximum_routes') == 0):
                                pass
                                l_2_value = '0 (no limit)'
                                _loop_vars['value'] = l_2_value
                            else:
                                pass
                                l_2_value = environment.getattr(l_2_neighbor, 'maximum_routes')
                                _loop_vars['value'] = l_2_value
                            if (t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit')) or t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_only'), True)):
                                pass
                                l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), ' (', ))
                                _loop_vars['value'] = l_2_value
                                if t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit')):
                                    pass
                                    l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), 'warning-limit ', environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit'), ))
                                    _loop_vars['value'] = l_2_value
                                    if t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_only'), True):
                                        pass
                                        l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), ', ', ))
                                        _loop_vars['value'] = l_2_value
                                    else:
                                        pass
                                        l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), ')', ))
                                        _loop_vars['value'] = l_2_value
                                if t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_only'), True):
                                    pass
                                    l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), 'warning-only)', ))
                                    _loop_vars['value'] = l_2_value
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['maximum_routes'] = t_1((undefined(name='value') if l_2_value is missing else l_2_value), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'maximum_routes'), '-')
                        if t_9(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'enabled'), True):
                            pass
                            if t_9(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times')):
                                pass
                                l_2_value_allowas = str_join(('Allowed, allowed ', environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times'), ' times', ))
                                _loop_vars['value_allowas'] = l_2_value_allowas
                            else:
                                pass
                                l_2_value_allowas = 'Allowed, allowed 3 (default) times'
                                _loop_vars['value_allowas'] = l_2_value_allowas
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['allowas_in'] = t_1((undefined(name='value_allowas') if l_2_value_allowas is missing else l_2_value_allowas), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'allowas_in'), '-')
                        if t_9(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled')):
                            pass
                            l_2_neighbor_rib_in_pre_policy_retain = environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled')
                            _loop_vars['neighbor_rib_in_pre_policy_retain'] = l_2_neighbor_rib_in_pre_policy_retain
                            if (t_9(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True) and t_9(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'all'), True)):
                                pass
                                l_2_neighbor_rib_in_pre_policy_retain = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain') if l_2_neighbor_rib_in_pre_policy_retain is missing else l_2_neighbor_rib_in_pre_policy_retain), ' (All)', ))
                                _loop_vars['neighbor_rib_in_pre_policy_retain'] = l_2_neighbor_rib_in_pre_policy_retain
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['rib_in_pre_policy_retain'] = t_1((undefined(name='neighbor_rib_in_pre_policy_retain') if l_2_neighbor_rib_in_pre_policy_retain is missing else l_2_neighbor_rib_in_pre_policy_retain), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'rib_in_pre_policy_retain'), '-')
                        yield '| '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'remote_as'))
                        yield ' | '
                        yield str(environment.getattr(l_1_vrf, 'name'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'shutdown'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'send_community'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'maximum_routes'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'allowas_in'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'bfd'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'rib_in_pre_policy_retain'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'route_reflector_client'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'passive'))
                        yield ' |\n'
                    l_2_neighbor = l_2_inherited_vrf = l_2_neighbor_peer_group = l_2_peer_group = l_2_active_parameter_vrf = l_2_value = l_2_value_allowas = l_2_neighbor_rib_in_pre_policy_retain = missing
            l_1_vrf = missing
        l_0_neighbor_interfaces = []
        context.vars['neighbor_interfaces'] = l_0_neighbor_interfaces
        context.exported_vars.add('neighbor_interfaces')
        for l_1_neighbor_interface in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbor_interfaces'), 'name'):
            _loop_vars = {}
            pass
            context.call(environment.getattr((undefined(name='neighbor_interfaces') if l_0_neighbor_interfaces is missing else l_0_neighbor_interfaces), 'append'), l_1_neighbor_interface, _loop_vars=_loop_vars)
        l_1_neighbor_interface = missing
        for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
            _loop_vars = {}
            pass
            for l_2_neighbor_interface in t_2(environment.getattr(l_1_vrf, 'neighbor_interfaces'), 'name'):
                _loop_vars = {}
                pass
                context.call(environment.getattr(l_2_neighbor_interface, 'update'), {'vrf': environment.getattr(l_1_vrf, 'name')}, _loop_vars=_loop_vars)
                context.call(environment.getattr((undefined(name='neighbor_interfaces') if l_0_neighbor_interfaces is missing else l_0_neighbor_interfaces), 'append'), l_2_neighbor_interface, _loop_vars=_loop_vars)
            l_2_neighbor_interface = missing
        l_1_vrf = missing
        if (t_5((undefined(name='neighbor_interfaces') if l_0_neighbor_interfaces is missing else l_0_neighbor_interfaces)) > 0):
            pass
            yield '\n#### BGP Neighbor Interfaces\n\n| Neighbor Interface | VRF | Peer Group | Remote AS | Peer Filter |\n| ------------------ | --- | ---------- | --------- | ----------- |\n'
            for l_1_neighbor_interface in (undefined(name='neighbor_interfaces') if l_0_neighbor_interfaces is missing else l_0_neighbor_interfaces):
                l_1_vrf = l_1_peer_group = l_1_remote_as = l_1_peer_filter = missing
                _loop_vars = {}
                pass
                l_1_vrf = t_1(environment.getattr(l_1_neighbor_interface, 'vrf'), 'default')
                _loop_vars['vrf'] = l_1_vrf
                l_1_peer_group = t_1(environment.getattr(l_1_neighbor_interface, 'peer_group'), '-')
                _loop_vars['peer_group'] = l_1_peer_group
                l_1_remote_as = t_1(environment.getattr(l_1_neighbor_interface, 'remote_as'), '-')
                _loop_vars['remote_as'] = l_1_remote_as
                l_1_peer_filter = t_1(environment.getattr(l_1_neighbor_interface, 'peer_filter'), '-')
                _loop_vars['peer_filter'] = l_1_peer_filter
                yield '| '
                yield str(environment.getattr(l_1_neighbor_interface, 'name'))
                yield ' | '
                yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                yield ' | '
                yield str((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group))
                yield ' | '
                yield str((undefined(name='remote_as') if l_1_remote_as is missing else l_1_remote_as))
                yield ' | '
                yield str((undefined(name='peer_filter') if l_1_peer_filter is missing else l_1_peer_filter))
                yield ' |\n'
            l_1_neighbor_interface = l_1_vrf = l_1_peer_group = l_1_remote_as = l_1_peer_filter = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'aggregate_addresses')):
            pass
            yield '\n#### BGP Route Aggregation\n\n| Prefix | AS Set | Advertise Map | Supress Map | Summary Only | Attribute Map | Match Map | Advertise Only |\n| ------ | ------ | ------------- | ----------- | ------------ | ------------- | --------- | -------------- |\n'
            for l_1_aggregate_address in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'aggregate_addresses'), 'prefix'):
                l_1_as_set = resolve('as_set')
                l_1_summary_only = resolve('summary_only')
                l_1_advertise_only = resolve('advertise_only')
                l_1_advertise_map = l_1_supress_map = l_1_attribute_map = l_1_match_map = missing
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_aggregate_address, 'as_set'), True):
                    pass
                    l_1_as_set = True
                    _loop_vars['as_set'] = l_1_as_set
                else:
                    pass
                    l_1_as_set = False
                    _loop_vars['as_set'] = l_1_as_set
                l_1_advertise_map = t_1(environment.getattr(l_1_aggregate_address, 'advertise_map'), '-')
                _loop_vars['advertise_map'] = l_1_advertise_map
                l_1_supress_map = t_1(environment.getattr(l_1_aggregate_address, 'supress_map'), '-')
                _loop_vars['supress_map'] = l_1_supress_map
                if t_9(environment.getattr(l_1_aggregate_address, 'summary_only'), True):
                    pass
                    l_1_summary_only = True
                    _loop_vars['summary_only'] = l_1_summary_only
                else:
                    pass
                    l_1_summary_only = False
                    _loop_vars['summary_only'] = l_1_summary_only
                l_1_attribute_map = t_1(environment.getattr(l_1_aggregate_address, 'attribute_map'), '-')
                _loop_vars['attribute_map'] = l_1_attribute_map
                l_1_match_map = t_1(environment.getattr(l_1_aggregate_address, 'match_map'), '-')
                _loop_vars['match_map'] = l_1_match_map
                if t_9(environment.getattr(l_1_aggregate_address, 'advertise_only'), True):
                    pass
                    l_1_advertise_only = True
                    _loop_vars['advertise_only'] = l_1_advertise_only
                else:
                    pass
                    l_1_advertise_only = False
                    _loop_vars['advertise_only'] = l_1_advertise_only
                yield '| '
                yield str(environment.getattr(l_1_aggregate_address, 'prefix'))
                yield ' | '
                yield str((undefined(name='as_set') if l_1_as_set is missing else l_1_as_set))
                yield ' | '
                yield str((undefined(name='advertise_map') if l_1_advertise_map is missing else l_1_advertise_map))
                yield ' | '
                yield str((undefined(name='supress_map') if l_1_supress_map is missing else l_1_supress_map))
                yield ' | '
                yield str((undefined(name='summary_only') if l_1_summary_only is missing else l_1_summary_only))
                yield ' | '
                yield str((undefined(name='attribute_map') if l_1_attribute_map is missing else l_1_attribute_map))
                yield ' | '
                yield str((undefined(name='match_map') if l_1_match_map is missing else l_1_match_map))
                yield ' | '
                yield str((undefined(name='advertise_only') if l_1_advertise_only is missing else l_1_advertise_only))
                yield ' |\n'
            l_1_aggregate_address = l_1_as_set = l_1_advertise_map = l_1_supress_map = l_1_summary_only = l_1_attribute_map = l_1_match_map = l_1_advertise_only = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn')):
            pass
            yield '\n#### Router BGP EVPN Address Family\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '\n- VPN import pruning is **enabled**\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop'), 'resolution_disabled'), True):
                pass
                yield '\n- Next-hop resolution is **disabled**\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_unchanged'), True):
                pass
                yield '- Next-hop-unchanged is explicitly configured (default behaviour)\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_mpls_resolution_ribs')):
                pass
                yield '\n'
                l_0_rib_position = ['Primary', 'Secondary', 'Tertiary']
                context.vars['rib_position'] = l_0_rib_position
                context.exported_vars.add('rib_position')
                l_1_loop = missing
                for l_1_rib, l_1_loop in LoopContext(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_mpls_resolution_ribs'), undefined):
                    l_1_evpn_mpls_resolution_rib = resolve('evpn_mpls_resolution_rib')
                    _loop_vars = {}
                    pass
                    if t_9(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib-colored'):
                        pass
                        l_1_evpn_mpls_resolution_rib = 'tunnel-rib-colored system-colored-tunnel-rib'
                        _loop_vars['evpn_mpls_resolution_rib'] = l_1_evpn_mpls_resolution_rib
                    elif (t_9(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib') and t_9(environment.getattr(l_1_rib, 'rib_name'))):
                        pass
                        l_1_evpn_mpls_resolution_rib = str_join(('tunnel-rib ', environment.getattr(l_1_rib, 'rib_name'), ))
                        _loop_vars['evpn_mpls_resolution_rib'] = l_1_evpn_mpls_resolution_rib
                    elif t_9(environment.getattr(l_1_rib, 'rib_type')):
                        pass
                        l_1_evpn_mpls_resolution_rib = environment.getattr(l_1_rib, 'rib_type')
                        _loop_vars['evpn_mpls_resolution_rib'] = l_1_evpn_mpls_resolution_rib
                    yield '- Next-hop MPLS resolution '
                    yield str(environment.getitem((undefined(name='rib_position') if l_0_rib_position is missing else l_0_rib_position), environment.getattr(l_1_loop, 'index0')))
                    yield '-RIB : '
                    yield str((undefined(name='evpn_mpls_resolution_rib') if l_1_evpn_mpls_resolution_rib is missing else l_1_evpn_mpls_resolution_rib))
                    yield '\n'
                l_1_loop = l_1_rib = l_1_evpn_mpls_resolution_rib = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups')):
                pass
                yield '\n##### EVPN Peer Groups\n\n| Peer Group | Activate | Encapsulation |\n| ---------- | -------- | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups'), 'name'):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'encapsulation'), 'default'))
                    yield ' |\n'
                l_1_peer_group = missing
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'encapsulation')):
                pass
                yield '\n##### EVPN Neighbor Default Encapsulation\n\n| Neighbor Default Encapsulation | Next-hop-self Source Interface |\n| ------------------------------ | ------------------------------ |\n'
                l_0_row_default_encapsulation = t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'encapsulation'), 'vxlan')
                context.vars['row_default_encapsulation'] = l_0_row_default_encapsulation
                context.exported_vars.add('row_default_encapsulation')
                l_0_row_nhs_source_interface = t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_source_interface'), '-')
                context.vars['row_nhs_source_interface'] = l_0_row_nhs_source_interface
                context.exported_vars.add('row_nhs_source_interface')
                yield '| '
                yield str((undefined(name='row_default_encapsulation') if l_0_row_default_encapsulation is missing else l_0_row_default_encapsulation))
                yield ' | '
                yield str((undefined(name='row_nhs_source_interface') if l_0_row_nhs_source_interface is missing else l_0_row_nhs_source_interface))
                yield ' |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection')):
                pass
                yield '\n##### EVPN Host Flapping Settings\n\n| State | Window | Threshold | Expiry Timeout |\n| ----- | ------ | --------- | -------------- |\n'
                l_0_evpn_hostflap_detection_window = '-'
                context.vars['evpn_hostflap_detection_window'] = l_0_evpn_hostflap_detection_window
                context.exported_vars.add('evpn_hostflap_detection_window')
                l_0_evpn_hostflap_detection_threshold = '-'
                context.vars['evpn_hostflap_detection_threshold'] = l_0_evpn_hostflap_detection_threshold
                context.exported_vars.add('evpn_hostflap_detection_threshold')
                l_0_evpn_hostflap_detection_expiry = '-'
                context.vars['evpn_hostflap_detection_expiry'] = l_0_evpn_hostflap_detection_expiry
                context.exported_vars.add('evpn_hostflap_detection_expiry')
                if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'enabled'), True):
                    pass
                    l_0_evpn_hostflap_detection_state = 'Enabled'
                    context.vars['evpn_hostflap_detection_state'] = l_0_evpn_hostflap_detection_state
                    context.exported_vars.add('evpn_hostflap_detection_state')
                    if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window')):
                        pass
                        l_0_evpn_hostflap_detection_window = str_join((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window'), ' Seconds', ))
                        context.vars['evpn_hostflap_detection_window'] = l_0_evpn_hostflap_detection_window
                        context.exported_vars.add('evpn_hostflap_detection_window')
                    l_0_evpn_hostflap_detection_threshold = t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'threshold'), '-')
                    context.vars['evpn_hostflap_detection_threshold'] = l_0_evpn_hostflap_detection_threshold
                    context.exported_vars.add('evpn_hostflap_detection_threshold')
                    if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout')):
                        pass
                        l_0_evpn_hostflap_detection_expiry = str_join((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout'), ' Seconds', ))
                        context.vars['evpn_hostflap_detection_expiry'] = l_0_evpn_hostflap_detection_expiry
                        context.exported_vars.add('evpn_hostflap_detection_expiry')
                else:
                    pass
                    l_0_evpn_hostflap_detection_state = 'Disabled'
                    context.vars['evpn_hostflap_detection_state'] = l_0_evpn_hostflap_detection_state
                    context.exported_vars.add('evpn_hostflap_detection_state')
                yield '| '
                yield str((undefined(name='evpn_hostflap_detection_state') if l_0_evpn_hostflap_detection_state is missing else l_0_evpn_hostflap_detection_state))
                yield ' | '
                yield str((undefined(name='evpn_hostflap_detection_window') if l_0_evpn_hostflap_detection_window is missing else l_0_evpn_hostflap_detection_window))
                yield ' | '
                yield str((undefined(name='evpn_hostflap_detection_threshold') if l_0_evpn_hostflap_detection_threshold is missing else l_0_evpn_hostflap_detection_threshold))
                yield ' | '
                yield str((undefined(name='evpn_hostflap_detection_expiry') if l_0_evpn_hostflap_detection_expiry is missing else l_0_evpn_hostflap_detection_expiry))
                yield ' |\n'
        l_0_evpn_gw_config = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), peer_groups=[], configured=False)
        context.vars['evpn_gw_config'] = l_0_evpn_gw_config
        context.exported_vars.add('evpn_gw_config')
        for l_1_peer_group in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), 'name'):
            l_1_address_family_evpn_peer_group = resolve('address_family_evpn_peer_group')
            _loop_vars = {}
            pass
            if (t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn')) and t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups'))):
                pass
                l_1_address_family_evpn_peer_group = t_6(context.eval_ctx, t_8(context, t_1(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups'), []), 'name', 'arista.avd.defined', environment.getattr(l_1_peer_group, 'name')))
                _loop_vars['address_family_evpn_peer_group'] = l_1_address_family_evpn_peer_group
                if t_9(environment.getattr(environment.getitem((undefined(name='address_family_evpn_peer_group') if l_1_address_family_evpn_peer_group is missing else l_1_address_family_evpn_peer_group), 0), 'domain_remote'), True):
                    pass
                    context.call(environment.getattr(environment.getattr((undefined(name='evpn_gw_config') if l_0_evpn_gw_config is missing else l_0_evpn_gw_config), 'peer_groups'), 'append'), environment.getattr(l_1_peer_group, 'name'), _loop_vars=_loop_vars)
                    if not isinstance(l_0_evpn_gw_config, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_0_evpn_gw_config['configured'] = True
        l_1_peer_group = l_1_address_family_evpn_peer_group = missing
        if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'enable'), True):
            pass
            if not isinstance(l_0_evpn_gw_config, Namespace):
                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
            l_0_evpn_gw_config['configured'] = True
        if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'inter_domain'), True):
            pass
            if not isinstance(l_0_evpn_gw_config, Namespace):
                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
            l_0_evpn_gw_config['configured'] = True
        if t_9(environment.getattr((undefined(name='evpn_gw_config') if l_0_evpn_gw_config is missing else l_0_evpn_gw_config), 'configured'), True):
            pass
            yield '\n##### EVPN DCI Gateway Summary\n\n| Settings | Value |\n| -------- | ----- |\n'
            if (t_5(environment.getattr((undefined(name='evpn_gw_config') if l_0_evpn_gw_config is missing else l_0_evpn_gw_config), 'peer_groups')) > 0):
                pass
                yield '| Remote Domain Peer Groups | '
                yield str(t_4(context.eval_ctx, environment.getattr((undefined(name='evpn_gw_config') if l_0_evpn_gw_config is missing else l_0_evpn_gw_config), 'peer_groups'), ', '))
                yield ' |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'enable'), True):
                pass
                yield '| L3 Gateway Configured | True |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'inter_domain'), True):
                pass
                yield '| L3 Gateway Inter-domain | True |\n'
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te')):
            pass
            yield '\n#### Router BGP IPv4 SR-TE Address Family\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'neighbors')):
                pass
                yield '\n##### IPv4 SR-TE Neighbors\n\n| Neighbor | Activate | Route-map In | Route-map Out |\n| -------- | -------- | ------------ | ------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'neighbors'), 'ip_address'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_neighbor, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_neighbor, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_neighbor = l_1_route_map_in = l_1_route_map_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'peer_groups')):
                pass
                yield '\n##### IPv4 SR-TE Peer Groups\n\n| Peer Group | Activate | Route-map In | Route-map Out |\n| ---------- | -------- | ------------ | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'peer_groups'), 'name'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_peer_group, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_peer_group, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_peer_group = l_1_route_map_in = l_1_route_map_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te')):
            pass
            yield '\n#### Router BGP IPv6 SR-TE Address Family\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'neighbors')):
                pass
                yield '\n##### IPv6 SR-TE Neighbors\n\n| Neighbor | Activate | Route-map In | Route-map Out |\n| -------- | -------- | ------------ | ------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'neighbors'), 'ip_address'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_neighbor, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_neighbor, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_neighbor = l_1_route_map_in = l_1_route_map_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'peer_groups')):
                pass
                yield '\n##### IPv6 SR-TE Peer Groups\n\n| Peer Group | Activate | Route-map In | Route-map Out |\n| ---------- | -------- | ------------ | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'peer_groups'), 'name'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_peer_group, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_peer_group, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_peer_group = l_1_route_map_in = l_1_route_map_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state')):
            pass
            yield '\n#### Router BGP Link-State Address Family\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'neighbors')):
                pass
                yield '\n##### Link-State Neighbors\n\n| Neighbor | Activate | Missing policy In action | Missing policy Out action |\n| -------- | -------- | ------------------------ | ------------------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'neighbors'), 'ip_address'):
                    l_1_missing_policy_in = l_1_missing_policy_out = missing
                    _loop_vars = {}
                    pass
                    l_1_missing_policy_in = t_1(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_in_action'), '-')
                    _loop_vars['missing_policy_in'] = l_1_missing_policy_in
                    l_1_missing_policy_out = t_1(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_out_action'), '-')
                    _loop_vars['missing_policy_out'] = l_1_missing_policy_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='missing_policy_in') if l_1_missing_policy_in is missing else l_1_missing_policy_in))
                    yield ' | '
                    yield str((undefined(name='missing_policy_out') if l_1_missing_policy_out is missing else l_1_missing_policy_out))
                    yield ' |\n'
                l_1_neighbor = l_1_missing_policy_in = l_1_missing_policy_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'peer_groups')):
                pass
                yield '\n##### Link-State Peer Groups\n\n| Peer Group | Activate | Missing policy In action | Missing policy Out action |\n| ---------- | -------- | ------------------------ | ------------------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'peer_groups'), 'name'):
                    l_1_missing_policy_in = l_1_missing_policy_out = missing
                    _loop_vars = {}
                    pass
                    l_1_missing_policy_in = t_1(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_in_action'), '-')
                    _loop_vars['missing_policy_in'] = l_1_missing_policy_in
                    l_1_missing_policy_out = t_1(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_out_action'), '-')
                    _loop_vars['missing_policy_out'] = l_1_missing_policy_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='missing_policy_in') if l_1_missing_policy_in is missing else l_1_missing_policy_in))
                    yield ' | '
                    yield str((undefined(name='missing_policy_out') if l_1_missing_policy_out is missing else l_1_missing_policy_out))
                    yield ' |\n'
                l_1_peer_group = l_1_missing_policy_in = l_1_missing_policy_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection')):
                pass
                yield '\n##### Link-State Path Selection Configuration\n\n| Settings | Value |\n| -------- | ----- |\n'
                if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles')):
                    pass
                    l_0_path_selection_roles = []
                    context.vars['path_selection_roles'] = l_0_path_selection_roles
                    context.exported_vars.add('path_selection_roles')
                    if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'producer'), True):
                        pass
                        context.call(environment.getattr((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), 'append'), 'producer')
                    if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'consumer'), True):
                        pass
                        context.call(environment.getattr((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), 'append'), 'consumer')
                    if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'propagator'), True):
                        pass
                        context.call(environment.getattr((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), 'append'), 'propagator')
                    yield '| Role(s) | '
                    yield str(t_4(context.eval_ctx, (undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), '<br>'))
                    yield ' |\n'
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4')):
            pass
            yield '\n#### Router BGP VPN-IPv4 Address Family\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '\n- VPN import pruning is **enabled**\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbors')):
                pass
                yield '\n##### VPN-IPv4 Neighbors\n\n| Neighbor | Activate | Route-map In | Route-map Out |\n| -------- | -------- | ------------ | ------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbors'), 'ip_address'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_neighbor, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_neighbor, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_neighbor = l_1_route_map_in = l_1_route_map_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'peer_groups')):
                pass
                yield '\n##### VPN-IPv4 Peer Groups\n\n| Peer Group | Activate | Route-map In | Route-map Out |\n| ---------- | -------- | ------------ | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'peer_groups'), 'name'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_peer_group, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_peer_group, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_peer_group = l_1_route_map_in = l_1_route_map_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6')):
            pass
            yield '\n#### Router BGP VPN-IPv6 Address Family\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '\n- VPN import pruning is **enabled**\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbors')):
                pass
                yield '\n##### VPN-IPv6 Neighbors\n\n| Neighbor | Activate | Route-map In | Route-map Out |\n| -------- | -------- | ------------ | ------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbors'), 'ip_address'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_neighbor, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_neighbor, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_neighbor = l_1_route_map_in = l_1_route_map_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'peer_groups')):
                pass
                yield '\n##### VPN-IPv6 Peer Groups\n\n| Peer Group | Activate | Route-map In | Route-map Out |\n| ---------- | -------- | ------------ | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'peer_groups'), 'name'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_peer_group, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_peer_group, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_peer_group = l_1_route_map_in = l_1_route_map_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection')):
            pass
            yield '\n#### Router BGP Path-Selection Address Family\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'neighbors')):
                pass
                yield '\n##### Path-Selection Neighbors\n\n| Neighbor | Activate |\n| -------- | -------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' |\n'
                l_1_neighbor = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'peer_groups')):
                pass
                yield '\n##### Path-Selection Peer Groups\n\n| Peer Group | Activate |\n| ---------- | -------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'peer_groups'), 'name'):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' |\n'
                l_1_peer_group = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlan_aware_bundles')):
            pass
            yield '\n#### Router BGP VLAN Aware Bundles\n\n| VLAN Aware Bundle | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute | VLANs |\n| ----------------- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ | ----- |\n'
            for l_1_vlan_aware_bundle in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlan_aware_bundles'), 'name'):
                l_1_both_route_target = resolve('both_route_target')
                l_1_import_route_target = resolve('import_route_target')
                l_1_export_route_target = resolve('export_route_target')
                l_1_route_distinguisher = l_1_vlans = l_1_redistribute_route = l_1_no_redistribute_route = l_1_redistribution = missing
                _loop_vars = {}
                pass
                l_1_route_distinguisher = t_1(environment.getattr(l_1_vlan_aware_bundle, 'rd'), '-')
                _loop_vars['route_distinguisher'] = l_1_route_distinguisher
                l_1_vlans = t_1(environment.getattr(l_1_vlan_aware_bundle, 'vlan'), '-')
                _loop_vars['vlans'] = l_1_vlans
                if (t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'both')) or t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_export_evpn_domains'))):
                    pass
                    l_1_both_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'both'), []))
                    _loop_vars['both_route_target'] = l_1_both_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_export_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='both_route_target') if l_1_both_route_target is missing else l_1_both_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                if (t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import')) or t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_evpn_domains'))):
                    pass
                    l_1_import_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import'), []))
                    _loop_vars['import_route_target'] = l_1_import_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='import_route_target') if l_1_import_route_target is missing else l_1_import_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                if (t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export')) or t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export_evpn_domains'))):
                    pass
                    l_1_export_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export'), []))
                    _loop_vars['export_route_target'] = l_1_export_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='export_route_target') if l_1_export_route_target is missing else l_1_export_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                l_1_redistribute_route = t_6(context.eval_ctx, t_1(environment.getattr(l_1_vlan_aware_bundle, 'redistribute_routes'), ''))
                _loop_vars['redistribute_route'] = l_1_redistribute_route
                l_1_no_redistribute_route = t_6(context.eval_ctx, t_7(context, t_1(environment.getattr(l_1_vlan_aware_bundle, 'no_redistribute_routes'), ''), 'replace', '', 'no ', 1))
                _loop_vars['no_redistribute_route'] = l_1_no_redistribute_route
                l_1_redistribution = ((undefined(name='redistribute_route') if l_1_redistribute_route is missing else l_1_redistribute_route) + (undefined(name='no_redistribute_route') if l_1_no_redistribute_route is missing else l_1_no_redistribute_route))
                _loop_vars['redistribution'] = l_1_redistribution
                yield '| '
                yield str(environment.getattr(l_1_vlan_aware_bundle, 'name'))
                yield ' | '
                yield str((undefined(name='route_distinguisher') if l_1_route_distinguisher is missing else l_1_route_distinguisher))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='both_route_target') if l_1_both_route_target is missing else l_1_both_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='import_route_target') if l_1_import_route_target is missing else l_1_import_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='export_route_target') if l_1_export_route_target is missing else l_1_export_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_1(t_4(context.eval_ctx, (undefined(name='redistribution') if l_1_redistribution is missing else l_1_redistribution), '<br>'), '-'))
                yield ' | '
                yield str((undefined(name='vlans') if l_1_vlans is missing else l_1_vlans))
                yield ' |\n'
            l_1_vlan_aware_bundle = l_1_route_distinguisher = l_1_vlans = l_1_both_route_target = l_1_import_route_target = l_1_export_route_target = l_1_redistribute_route = l_1_no_redistribute_route = l_1_redistribution = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans')):
            pass
            yield '\n#### Router BGP VLANs\n\n| VLAN | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute |\n| ---- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ |\n'
            for l_1_vlan in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans'), 'id'):
                l_1_both_route_target = resolve('both_route_target')
                l_1_import_route_target = resolve('import_route_target')
                l_1_export_route_target = resolve('export_route_target')
                l_1_route_distinguisher = l_1_redistribute_route = l_1_no_redistribute_route = l_1_redistribution = missing
                _loop_vars = {}
                pass
                l_1_route_distinguisher = t_1(environment.getattr(l_1_vlan, 'rd'), '-')
                _loop_vars['route_distinguisher'] = l_1_route_distinguisher
                if (t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'both')) or t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_export_evpn_domains'))):
                    pass
                    l_1_both_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'both'), []))
                    _loop_vars['both_route_target'] = l_1_both_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_export_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='both_route_target') if l_1_both_route_target is missing else l_1_both_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                if (t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import')) or t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_evpn_domains'))):
                    pass
                    l_1_import_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import'), []))
                    _loop_vars['import_route_target'] = l_1_import_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='import_route_target') if l_1_import_route_target is missing else l_1_import_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                if (t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export')) or t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export_evpn_domains'))):
                    pass
                    l_1_export_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export'), []))
                    _loop_vars['export_route_target'] = l_1_export_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='export_route_target') if l_1_export_route_target is missing else l_1_export_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                l_1_redistribute_route = t_6(context.eval_ctx, t_1(environment.getattr(l_1_vlan, 'redistribute_routes'), ''))
                _loop_vars['redistribute_route'] = l_1_redistribute_route
                l_1_no_redistribute_route = t_6(context.eval_ctx, t_7(context, t_1(environment.getattr(l_1_vlan, 'no_redistribute_routes'), ''), 'replace', '', 'no ', 1))
                _loop_vars['no_redistribute_route'] = l_1_no_redistribute_route
                l_1_redistribution = ((undefined(name='redistribute_route') if l_1_redistribute_route is missing else l_1_redistribute_route) + (undefined(name='no_redistribute_route') if l_1_no_redistribute_route is missing else l_1_no_redistribute_route))
                _loop_vars['redistribution'] = l_1_redistribution
                yield '| '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield ' | '
                yield str((undefined(name='route_distinguisher') if l_1_route_distinguisher is missing else l_1_route_distinguisher))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='both_route_target') if l_1_both_route_target is missing else l_1_both_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='import_route_target') if l_1_import_route_target is missing else l_1_import_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='export_route_target') if l_1_export_route_target is missing else l_1_export_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_1(t_4(context.eval_ctx, (undefined(name='redistribution') if l_1_redistribution is missing else l_1_redistribution), '<br>'), '-'))
                yield ' |\n'
            l_1_vlan = l_1_route_distinguisher = l_1_both_route_target = l_1_import_route_target = l_1_export_route_target = l_1_redistribute_route = l_1_no_redistribute_route = l_1_redistribution = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws')):
            pass
            yield '\n#### Router BGP VPWS Instances\n\n| Instance | Route-Distinguisher | Both Route-Target | MPLS Control Word | Label Flow | MTU | Pseudowire | Local ID | Remote ID |\n| -------- | ------------------- | ----------------- | ----------------- | -----------| --- | ---------- | -------- | --------- |\n'
            for l_1_vpws_service in environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws'):
                _loop_vars = {}
                pass
                if ((t_9(environment.getattr(l_1_vpws_service, 'name')) and t_9(environment.getattr(l_1_vpws_service, 'rd'))) and t_9(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export'))):
                    pass
                    for l_2_pseudowire in t_2(environment.getattr(l_1_vpws_service, 'pseudowires'), 'name'):
                        l_2_row_mpls_control_word = resolve('row_mpls_control_word')
                        l_2_row_label_flow = resolve('row_label_flow')
                        l_2_row_mtu = resolve('row_mtu')
                        _loop_vars = {}
                        pass
                        if t_9(environment.getattr(l_2_pseudowire, 'name')):
                            pass
                            l_2_row_mpls_control_word = t_1(environment.getattr(l_1_vpws_service, 'mpls_control_word'), False)
                            _loop_vars['row_mpls_control_word'] = l_2_row_mpls_control_word
                            l_2_row_label_flow = t_1(environment.getattr(l_1_vpws_service, 'label_flow'), False)
                            _loop_vars['row_label_flow'] = l_2_row_label_flow
                            l_2_row_mtu = t_1(environment.getattr(l_1_vpws_service, 'mtu'), '-')
                            _loop_vars['row_mtu'] = l_2_row_mtu
                            yield '| '
                            yield str(environment.getattr(l_1_vpws_service, 'name'))
                            yield ' | '
                            yield str(environment.getattr(l_1_vpws_service, 'rd'))
                            yield ' | '
                            yield str(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export'))
                            yield ' | '
                            yield str((undefined(name='row_mpls_control_word') if l_2_row_mpls_control_word is missing else l_2_row_mpls_control_word))
                            yield ' | '
                            yield str((undefined(name='row_label_flow') if l_2_row_label_flow is missing else l_2_row_label_flow))
                            yield ' | '
                            yield str((undefined(name='row_mtu') if l_2_row_mtu is missing else l_2_row_mtu))
                            yield ' | '
                            yield str(environment.getattr(l_2_pseudowire, 'name'))
                            yield ' | '
                            yield str(environment.getattr(l_2_pseudowire, 'id_local'))
                            yield ' | '
                            yield str(environment.getattr(l_2_pseudowire, 'id_remote'))
                            yield ' |\n'
                    l_2_pseudowire = l_2_row_mpls_control_word = l_2_row_label_flow = l_2_row_mtu = missing
            l_1_vpws_service = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs')):
            pass
            yield '\n#### Router BGP VRFs\n\n'
            if t_6(context.eval_ctx, t_8(context, environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'evpn_multicast', 'arista.avd.defined', True)):
                pass
                yield '| VRF | Route-Distinguisher | Redistribute | EVPN Multicast |\n| --- | ------------------- | ------------ | -------------- |\n'
            else:
                pass
                yield '| VRF | Route-Distinguisher | Redistribute |\n| --- | ------------------- | ------------ |\n'
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                l_1_route_distinguisher = l_1_redistribute = l_1_multicast = l_1_multicast_transit = l_1_multicast_out = missing
                _loop_vars = {}
                pass
                l_1_route_distinguisher = t_1(environment.getattr(l_1_vrf, 'rd'), '-')
                _loop_vars['route_distinguisher'] = l_1_route_distinguisher
                l_1_redistribute = t_7(context, t_1(environment.getattr(l_1_vrf, 'redistribute_routes'), [{'source_protocol': '-'}]), attribute='source_protocol')
                _loop_vars['redistribute'] = l_1_redistribute
                l_1_multicast = t_1(environment.getattr(l_1_vrf, 'evpn_multicast'), False)
                _loop_vars['multicast'] = l_1_multicast
                l_1_multicast_transit = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4'), 'transit'), False)
                _loop_vars['multicast_transit'] = l_1_multicast_transit
                l_1_multicast_out = []
                _loop_vars['multicast_out'] = l_1_multicast_out
                context.call(environment.getattr((undefined(name='multicast_out') if l_1_multicast_out is missing else l_1_multicast_out), 'append'), str_join(('IPv4: ', (undefined(name='multicast') if l_1_multicast is missing else l_1_multicast), )), _loop_vars=_loop_vars)
                context.call(environment.getattr((undefined(name='multicast_out') if l_1_multicast_out is missing else l_1_multicast_out), 'append'), str_join(('Transit: ', (undefined(name='multicast_transit') if l_1_multicast_transit is missing else l_1_multicast_transit), )), _loop_vars=_loop_vars)
                if t_6(context.eval_ctx, t_8(context, environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'evpn_multicast', 'arista.avd.defined', True)):
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_vrf, 'name'))
                    yield ' | '
                    yield str((undefined(name='route_distinguisher') if l_1_route_distinguisher is missing else l_1_route_distinguisher))
                    yield ' | '
                    yield str(t_4(context.eval_ctx, (undefined(name='redistribute') if l_1_redistribute is missing else l_1_redistribute), '<br>'))
                    yield ' | '
                    yield str(t_4(context.eval_ctx, (undefined(name='multicast_out') if l_1_multicast_out is missing else l_1_multicast_out), '<br>'))
                    yield ' |\n'
                else:
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_vrf, 'name'))
                    yield ' | '
                    yield str((undefined(name='route_distinguisher') if l_1_route_distinguisher is missing else l_1_route_distinguisher))
                    yield ' | '
                    yield str(t_4(context.eval_ctx, (undefined(name='redistribute') if l_1_redistribute is missing else l_1_redistribute), '<br>'))
                    yield ' |\n'
            l_1_vrf = l_1_route_distinguisher = l_1_redistribute = l_1_multicast = l_1_multicast_transit = l_1_multicast_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'session_trackers')):
            pass
            yield '\n#### Router BGP Session Trackers\n\n| Session Tracker Name | Recovery Delay (in seconds) |\n| -------------------- | --------------------------- |\n'
            for l_1_session_tracker in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'session_trackers'), 'name'):
                _loop_vars = {}
                pass
                yield '| '
                yield str(environment.getattr(l_1_session_tracker, 'name'))
                yield ' | '
                yield str(environment.getattr(l_1_session_tracker, 'recovery_delay'))
                yield ' |\n'
            l_1_session_tracker = missing
        yield '\n#### Router BGP Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/router-bgp.j2', 'documentation/router-bgp.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'distance_cli': l_0_distance_cli, 'evpn_gw_config': l_0_evpn_gw_config, 'evpn_hostflap_detection_expiry': l_0_evpn_hostflap_detection_expiry, 'evpn_hostflap_detection_state': l_0_evpn_hostflap_detection_state, 'evpn_hostflap_detection_threshold': l_0_evpn_hostflap_detection_threshold, 'evpn_hostflap_detection_window': l_0_evpn_hostflap_detection_window, 'neighbor_interfaces': l_0_neighbor_interfaces, 'path_selection_roles': l_0_path_selection_roles, 'paths_cli': l_0_paths_cli, 'rib_position': l_0_rib_position, 'row_default_encapsulation': l_0_row_default_encapsulation, 'row_nhs_source_interface': l_0_row_nhs_source_interface, 'rr_preserve_attributes_cli': l_0_rr_preserve_attributes_cli, 'temp': l_0_temp})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '7=81&11=84&17=86&18=90&22=93&24=97&28=100&29=104&31=107&32=109&33=112&35=114&36=117&40=120&42=123&43=125&44=128&45=130&49=133&52=136&55=139&58=142&60=145&63=148&65=151&68=154&69=156&70=159&71=161&73=165&75=167&76=169&77=172&78=174&80=178&82=180&83=182&84=185&85=187&87=191&91=193&92=196&93=199&94=201&95=204&96=206&97=209&101=211&108=214&110=216&109=220&111=224&112=226&113=228&114=230&116=233&120=244&121=247&123=249&122=253&124=257&125=259&126=261&127=263&129=266&134=280&137=283&139=292&143=294&144=297&146=299&147=302&149=304&150=306&151=308&152=310&153=312&154=314&157=317&159=319&160=321&161=323&162=325&164=328&166=330&167=333&169=335&170=338&172=340&173=343&175=345&178=348&179=351&181=353&184=356&187=359&188=362&190=364&191=366&192=368&193=370&195=373&197=375&200=378&201=380&202=383&204=385&205=388&207=390&208=393&210=395&213=398&214=401&216=403&217=406&219=408&220=410&221=412&223=416&225=418&226=420&227=422&228=424&229=426&230=428&232=432&235=434&236=436&239=439&241=441&242=443&243=445&244=447&246=450&248=452&253=456&254=459&255=462&256=464&257=467&258=469&259=472&263=474&269=477&270=487&271=489&272=491&273=493&276=495&277=497&279=500&280=502&282=505&283=507&285=510&286=512&288=515&289=517&291=520&292=522&293=525&294=527&297=530&298=532&300=535&301=537&303=540&304=542&306=545&307=547&309=550&310=552&313=555&314=557&315=560&316=563&317=566&318=569&319=572&320=574&322=577&323=579&325=582&326=585&327=588&328=590&329=592&330=594&333=596&334=599&335=602&336=604&337=606&339=610&341=612&342=614&343=616&344=618&345=620&346=622&348=626&351=628&352=630&356=632&357=635&358=637&359=639&361=643&364=645&365=647&366=651&368=676&369=679&370=681&371=690&372=692&373=694&374=696&377=698&378=700&380=703&381=705&383=708&384=710&386=713&387=715&389=718&390=720&391=723&392=725&395=728&396=730&398=733&399=735&401=738&402=740&404=743&405=745&408=748&409=750&410=753&411=756&412=759&413=762&414=764&416=767&417=769&419=772&420=775&421=778&422=781&423=783&424=785&426=789&428=791&429=793&430=795&431=797&432=799&433=801&435=805&438=807&439=809&443=811&444=814&445=816&446=818&448=822&451=824&452=827&453=829&454=831&455=833&458=835&459=839&464=863&465=866&466=869&468=871&469=874&470=877&471=878&474=881&480=884&481=888&482=890&483=892&484=894&485=897&488=908&494=911&495=918&496=920&498=924&500=926&501=928&502=930&503=932&505=936&507=938&508=940&509=942&510=944&512=948&514=951&517=968&520=971&524=974&528=977&531=980&533=983&534=987&535=991&536=993&537=995&538=997&539=999&540=1001&542=1004&545=1009&551=1012&552=1016&555=1023&561=1026&562=1029&563=1033&565=1037&571=1040&572=1043&573=1046&574=1049&575=1051&576=1054&577=1056&579=1059&580=1062&581=1064&584=1069&586=1073&589=1081&590=1084&591=1088&592=1090&594=1092&595=1094&596=1095&600=1099&601=1101&603=1104&604=1106&606=1109&612=1112&613=1115&615=1117&618=1120&622=1123&625=1126&631=1129&632=1133&633=1135&634=1138&637=1147&643=1150&644=1154&645=1156&646=1159&650=1168&653=1171&659=1174&660=1178&661=1180&662=1183&665=1192&671=1195&672=1199&673=1201&674=1204&678=1213&681=1216&687=1219&688=1223&689=1225&690=1228&693=1237&699=1240&700=1244&701=1246&702=1249&705=1258&711=1261&712=1263&713=1266&714=1268&716=1269&717=1271&719=1272&720=1274&722=1276&726=1278&729=1281&733=1284&739=1287&740=1291&741=1293&742=1296&745=1305&751=1308&752=1312&753=1314&754=1317&758=1326&761=1329&765=1332&771=1335&772=1339&773=1341&774=1344&777=1353&783=1356&784=1360&785=1362&786=1365&790=1374&793=1377&799=1380&800=1384&803=1389&809=1392&810=1396&814=1401&820=1404&821=1411&822=1413&823=1415&824=1417&825=1419&826=1422&829=1424&830=1426&831=1428&832=1431&835=1433&836=1435&837=1437&838=1440&841=1442&842=1444&843=1446&844=1449&847=1464&853=1467&854=1474&855=1476&856=1478&857=1480&858=1483&861=1485&862=1487&863=1489&864=1492&867=1494&868=1496&869=1498&870=1501&873=1503&874=1505&875=1507&876=1510&879=1523&885=1526&886=1529&887=1531&888=1537&889=1539&890=1541&891=1543&892=1546&898=1566&902=1569&909=1575&910=1579&911=1581&912=1583&913=1585&914=1587&915=1589&916=1590&917=1591&918=1594&920=1605&924=1612&930=1615&931=1619&938=1625'