from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-bgp.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_bgp = resolve('router_bgp')
    l_0_distance_cli = resolve('distance_cli')
    l_0_rr_preserve_attributes_cli = resolve('rr_preserve_attributes_cli')
    l_0_paths_cli = resolve('paths_cli')
    l_0_bgp_vlans = resolve('bgp_vlans')
    l_0_hostflap_detection_cli = resolve('hostflap_detection_cli')
    l_0_evpn_neighbor_default_encap_cli = resolve('evpn_neighbor_default_encap_cli')
    l_0_evpn_mpls_resolution_ribs = resolve('evpn_mpls_resolution_ribs')
    l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli = resolve('evpn_neighbor_default_nhs_received_evpn_routes_cli')
    l_0_path_selection_roles = resolve('path_selection_roles')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.hide_passwords']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.hide_passwords' found.")
    try:
        t_3 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_4 = environment.filters['indent']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'indent' found.")
    try:
        t_5 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_6 = environment.filters['sort']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No filter named 'sort' found.")
    try:
        t_7 = environment.filters['string']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No filter named 'string' found.")
    try:
        t_8 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_8(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    try:
        t_9 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_9(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    try:
        t_10 = environment.tests['number']
    except KeyError:
        @internalcode
        def t_10(*unused):
            raise TemplateRuntimeError("No test named 'number' found.")
    pass
    if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as')):
        pass
        yield '!\nrouter bgp '
        yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as'))
        yield '\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as_notation')):
            pass
            yield '   bgp asn notation '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as_notation'))
            yield '\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'router_id')):
            pass
            yield '   router-id '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'router_id'))
            yield '\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes')):
            pass
            l_0_distance_cli = str_join(('distance bgp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes'), ))
            context.vars['distance_cli'] = l_0_distance_cli
            context.exported_vars.add('distance_cli')
            if (t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes')) and t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'))):
                pass
                l_0_distance_cli = str_join(((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes'), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'), ))
                context.vars['distance_cli'] = l_0_distance_cli
                context.exported_vars.add('distance_cli')
            yield '   '
            yield str((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli))
            yield '\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'enabled'), True):
            pass
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time')):
                pass
                yield '   graceful-restart restart-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time')):
                pass
                yield '   graceful-restart stalepath-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time'))
                yield '\n'
            yield '   graceful-restart\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), False):
            pass
            yield '   no graceful-restart-helper\n'
        elif t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), True):
            pass
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time')):
                pass
                yield '   graceful-restart-helper restart-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time'))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'long_lived'), True):
                pass
                yield '   graceful-restart-helper long-lived\n'
        if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'enabled'), True):
            pass
            l_0_rr_preserve_attributes_cli = 'bgp route-reflector preserve-attributes'
            context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
            context.exported_vars.add('rr_preserve_attributes_cli')
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'always'), True):
                pass
                l_0_rr_preserve_attributes_cli = str_join(((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli), ' always', ))
                context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
                context.exported_vars.add('rr_preserve_attributes_cli')
            yield '   '
            yield str((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli))
            yield '\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths')):
            pass
            l_0_paths_cli = str_join(('maximum-paths ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths'), ))
            context.vars['paths_cli'] = l_0_paths_cli
            context.exported_vars.add('paths_cli')
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp')):
                pass
                l_0_paths_cli = str_join(((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli), ' ecmp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp'), ))
                context.vars['paths_cli'] = l_0_paths_cli
                context.exported_vars.add('paths_cli')
            yield '   '
            yield str((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli))
            yield '\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_for_convergence'), True):
            pass
            yield '   update wait-for-convergence\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_install'), True):
            pass
            yield '   update wait-install\n'
        if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), True):
            pass
            yield '   bgp default ipv4-unicast\n'
        elif t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), False):
            pass
            yield '   no bgp default ipv4-unicast\n'
        if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), True):
            pass
            yield '   bgp default ipv4-unicast transport ipv6\n'
        elif t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), False):
            pass
            yield '   no bgp default ipv4-unicast transport ipv6\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id')):
            pass
            yield '   bgp cluster-id '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id'))
            yield '\n'
        for l_1_bgp_default in t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_defaults'), []):
            _loop_vars = {}
            pass
            yield '   '
            yield str(l_1_bgp_default)
            yield '\n'
        l_1_bgp_default = missing
        if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'bestpath'), 'd_path'), True):
            pass
            yield '   bgp bestpath d-path\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges')):
            pass
            def t_11(fiter):
                for l_1_listen_range in fiter:
                    if ((t_8(environment.getattr(l_1_listen_range, 'peer_group')) and t_8(environment.getattr(l_1_listen_range, 'prefix'))) and (t_8(environment.getattr(l_1_listen_range, 'peer_filter')) or t_8(environment.getattr(l_1_listen_range, 'remote_as')))):
                        yield l_1_listen_range
            for l_1_listen_range in t_11(t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges'), 'peer_group')):
                l_1_listen_range_cli = missing
                _loop_vars = {}
                pass
                l_1_listen_range_cli = str_join(('bgp listen range ', environment.getattr(l_1_listen_range, 'prefix'), ))
                _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                if t_8(environment.getattr(l_1_listen_range, 'peer_id_include_router_id'), True):
                    pass
                    l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' peer-id include router-id', ))
                    _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' peer-group ', environment.getattr(l_1_listen_range, 'peer_group'), ))
                _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                if t_8(environment.getattr(l_1_listen_range, 'peer_filter')):
                    pass
                    l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' peer-filter ', environment.getattr(l_1_listen_range, 'peer_filter'), ))
                    _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                elif t_8(environment.getattr(l_1_listen_range, 'remote_as')):
                    pass
                    l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' remote-as ', environment.getattr(l_1_listen_range, 'remote_as'), ))
                    _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                yield '   '
                yield str((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli))
                yield '\n'
            l_1_listen_range = l_1_listen_range_cli = missing
        for l_1_peer_group in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), 'name'):
            _loop_vars = {}
            pass
            if (t_8(environment.getattr(l_1_peer_group, 'bgp_listen_range_prefix')) and t_8(environment.getattr(l_1_peer_group, 'peer_filter'))):
                pass
                yield '   bgp listen range '
                yield str(environment.getattr(l_1_peer_group, 'bgp_listen_range_prefix'))
                yield ' peer-group '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' peer-filter '
                yield str(environment.getattr(l_1_peer_group, 'peer_filter'))
                yield '\n'
        l_1_peer_group = missing
        for l_1_peer_group in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), 'name'):
            l_1_remove_private_as_cli = resolve('remove_private_as_cli')
            l_1_remove_private_as_ingress_cli = resolve('remove_private_as_ingress_cli')
            l_1_allowas_in_cli = resolve('allowas_in_cli')
            l_1_neighbor_rib_in_pre_policy_retain_cli = resolve('neighbor_rib_in_pre_policy_retain_cli')
            l_1_hide_passwords = resolve('hide_passwords')
            l_1_default_originate_cli = resolve('default_originate_cli')
            l_1_maximum_routes_cli = resolve('maximum_routes_cli')
            l_1_link_bandwidth_cli = resolve('link_bandwidth_cli')
            _loop_vars = {}
            pass
            if t_8(environment.getattr(l_1_peer_group, 'shutdown'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' shutdown\n'
            yield '   neighbor '
            yield str(environment.getattr(l_1_peer_group, 'name'))
            yield ' peer group\n'
            if t_8(environment.getattr(l_1_peer_group, 'remote_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' remote-as '
                yield str(environment.getattr(l_1_peer_group, 'remote_as'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'local_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' local-as '
                yield str(environment.getattr(l_1_peer_group, 'local_as'))
                yield ' no-prepend replace-as\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'as_path'), 'remote_as_replace_out'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' as-path remote-as replace out\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'as_path'), 'prepend_own_disabled'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' as-path prepend-own disabled\n'
            if t_8(environment.getattr(l_1_peer_group, 'next_hop_self'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' next-hop-self\n'
            if t_8(environment.getattr(l_1_peer_group, 'next_hop_unchanged'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' next-hop-unchanged\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled'), True):
                pass
                l_1_remove_private_as_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' remove-private-as', ))
                _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'all'), True):
                    pass
                    l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' all', ))
                    _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'replace_as'), True):
                        pass
                        l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' replace-as', ))
                        _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                yield '   '
                yield str((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' remove-private-as\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled'), True):
                pass
                l_1_remove_private_as_ingress_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' remove-private-as ingress', ))
                _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'replace_as'), True):
                    pass
                    l_1_remove_private_as_ingress_cli = str_join(((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli), ' replace-as', ))
                    _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                yield '   '
                yield str((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' remove-private-as ingress\n'
            if t_8(environment.getattr(l_1_peer_group, 'update_source')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' update-source '
                yield str(environment.getattr(l_1_peer_group, 'update_source'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'description')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' description '
                yield str(environment.getattr(l_1_peer_group, 'description'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'route_reflector_client'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' route-reflector-client\n'
            if t_8(environment.getattr(l_1_peer_group, 'bfd'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' bfd\n'
                if ((t_8(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'interval')) and t_8(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'min_rx'))) and t_8(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'multiplier'))):
                    pass
                    yield '   neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' bfd interval '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'interval'))
                    yield ' min-rx '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'min_rx'))
                    yield ' multiplier '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'multiplier'))
                    yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'enabled'), True):
                pass
                l_1_allowas_in_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' allowas-in', ))
                _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'times')):
                    pass
                    l_1_allowas_in_cli = str_join(((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli), ' ', environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'times'), ))
                    _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                yield '   '
                yield str((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled'), True):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'all'), True):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli), ' all', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled'), False):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('no neighbor ', environment.getattr(l_1_peer_group, 'name'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'ebgp_multihop')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' ebgp-multihop '
                yield str(environment.getattr(l_1_peer_group, 'ebgp_multihop'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'ttl_maximum_hops')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' ttl maximum-hops '
                yield str(environment.getattr(l_1_peer_group, 'ttl_maximum_hops'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'password')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' password 7 '
                yield str(t_2(environment.getattr(l_1_peer_group, 'password'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'enabled'), True):
                pass
                l_1_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-originate', ))
                _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map')):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map'), ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'always'), True):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' always', ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                yield '   '
                yield str((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'passive'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' passive\n'
            if t_8(environment.getattr(l_1_peer_group, 'session_tracker')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' session tracker '
                yield str(environment.getattr(l_1_peer_group, 'session_tracker'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'send_community'), 'all'):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' send-community\n'
            elif t_8(environment.getattr(l_1_peer_group, 'send_community')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' send-community '
                yield str(environment.getattr(l_1_peer_group, 'send_community'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'maximum_routes')):
                pass
                l_1_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' maximum-routes ', environment.getattr(l_1_peer_group, 'maximum_routes'), ))
                _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_8(environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit')):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-limit ', environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit'), ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_8(environment.getattr(l_1_peer_group, 'maximum_routes_warning_only'), True):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-only', ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                yield '   '
                yield str((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'enabled'), True):
                pass
                l_1_link_bandwidth_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' link-bandwidth', ))
                _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default')):
                    pass
                    l_1_link_bandwidth_cli = str_join(((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli), ' default ', environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default'), ))
                    _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                yield '   '
                yield str((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'weight')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' weight '
                yield str(environment.getattr(l_1_peer_group, 'weight'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'timers')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' timers '
                yield str(environment.getattr(l_1_peer_group, 'timers'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' route-map '
                yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                yield ' in\n'
            if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' route-map '
                yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                yield ' out\n'
        l_1_peer_group = l_1_remove_private_as_cli = l_1_remove_private_as_ingress_cli = l_1_allowas_in_cli = l_1_neighbor_rib_in_pre_policy_retain_cli = l_1_hide_passwords = l_1_default_originate_cli = l_1_maximum_routes_cli = l_1_link_bandwidth_cli = missing
        for l_1_neighbor_interface in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbor_interfaces'), 'name'):
            _loop_vars = {}
            pass
            if (t_8(environment.getattr(l_1_neighbor_interface, 'peer_group')) and t_8(environment.getattr(l_1_neighbor_interface, 'remote_as'))):
                pass
                yield '   neighbor interface '
                yield str(environment.getattr(l_1_neighbor_interface, 'name'))
                yield ' peer-group '
                yield str(environment.getattr(l_1_neighbor_interface, 'peer_group'))
                yield ' remote-as '
                yield str(environment.getattr(l_1_neighbor_interface, 'remote_as'))
                yield '\n'
            elif (t_8(environment.getattr(l_1_neighbor_interface, 'peer_group')) and t_8(environment.getattr(l_1_neighbor_interface, 'peer_filter'))):
                pass
                yield '   neighbor interface '
                yield str(environment.getattr(l_1_neighbor_interface, 'name'))
                yield ' peer-group '
                yield str(environment.getattr(l_1_neighbor_interface, 'peer_group'))
                yield ' peer-filter '
                yield str(environment.getattr(l_1_neighbor_interface, 'peer_filter'))
                yield '\n'
        l_1_neighbor_interface = missing
        for l_1_neighbor in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbors'), 'ip_address'):
            l_1_remove_private_as_cli = resolve('remove_private_as_cli')
            l_1_remove_private_as_ingress_cli = resolve('remove_private_as_ingress_cli')
            l_1_allowas_in_cli = resolve('allowas_in_cli')
            l_1_neighbor_rib_in_pre_policy_retain_cli = resolve('neighbor_rib_in_pre_policy_retain_cli')
            l_1_hide_passwords = resolve('hide_passwords')
            l_1_default_originate_cli = resolve('default_originate_cli')
            l_1_maximum_routes_cli = resolve('maximum_routes_cli')
            l_1_link_bandwidth_cli = resolve('link_bandwidth_cli')
            _loop_vars = {}
            pass
            if t_8(environment.getattr(l_1_neighbor, 'peer_group')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' peer group '
                yield str(environment.getattr(l_1_neighbor, 'peer_group'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'remote_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' remote-as '
                yield str(environment.getattr(l_1_neighbor, 'remote_as'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'next_hop_self'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' next-hop-self\n'
            if t_8(environment.getattr(l_1_neighbor, 'shutdown'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' shutdown\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'enabled'), True):
                pass
                l_1_remove_private_as_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' remove-private-as', ))
                _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'all'), True):
                    pass
                    l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' all', ))
                    _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                    if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'replace_as'), True):
                        pass
                        l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' replace-as', ))
                        _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                yield '   '
                yield str((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' remove-private-as\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as_ingress'), 'enabled'), True):
                pass
                l_1_remove_private_as_ingress_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' remove-private-as ingress', ))
                _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as_ingress'), 'replace_as'), True):
                    pass
                    l_1_remove_private_as_ingress_cli = str_join(((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli), ' replace-as', ))
                    _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                yield '   '
                yield str((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as_ingress'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' remove-private-as ingress\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'as_path'), 'remote_as_replace_out'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' as-path remote-as replace out\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'as_path'), 'prepend_own_disabled'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' as-path prepend-own disabled\n'
            if t_8(environment.getattr(l_1_neighbor, 'local_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' local-as '
                yield str(environment.getattr(l_1_neighbor, 'local_as'))
                yield ' no-prepend replace-as\n'
            if t_8(environment.getattr(l_1_neighbor, 'description')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' description '
                yield str(environment.getattr(l_1_neighbor, 'description'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'route_reflector_client'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-reflector-client\n'
            elif t_8(environment.getattr(l_1_neighbor, 'route_reflector_client'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-reflector-client\n'
            if t_8(environment.getattr(l_1_neighbor, 'ebgp_multihop')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' ebgp-multihop '
                yield str(environment.getattr(l_1_neighbor, 'ebgp_multihop'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'ttl_maximum_hops')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' ttl maximum-hops '
                yield str(environment.getattr(l_1_neighbor, 'ttl_maximum_hops'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'update_source')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' update-source '
                yield str(environment.getattr(l_1_neighbor, 'update_source'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'bfd'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' bfd\n'
                if ((t_8(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'interval')) and t_8(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'min_rx'))) and t_8(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'multiplier'))):
                    pass
                    yield '   neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' bfd interval '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'interval'))
                    yield ' min-rx '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'min_rx'))
                    yield ' multiplier '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'multiplier'))
                    yield '\n'
            elif (t_8(environment.getattr(l_1_neighbor, 'bfd'), False) and t_8(environment.getattr(l_1_neighbor, 'peer_group'))):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' bfd\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'enabled'), True):
                pass
                l_1_allowas_in_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' allowas-in', ))
                _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times')):
                    pass
                    l_1_allowas_in_cli = str_join(((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli), ' ', environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times'), ))
                    _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                yield '   '
                yield str((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'all'), True):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli), ' all', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), False):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('no neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'password')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' password 7 '
                yield str(t_2(environment.getattr(l_1_neighbor, 'password'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'passive'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' passive\n'
            if t_8(environment.getattr(l_1_neighbor, 'weight')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' weight '
                yield str(environment.getattr(l_1_neighbor, 'weight'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'session_tracker')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' session tracker '
                yield str(environment.getattr(l_1_neighbor, 'session_tracker'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'timers')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' timers '
                yield str(environment.getattr(l_1_neighbor, 'timers'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-map '
                yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                yield ' in\n'
            if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-map '
                yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                yield ' out\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'enabled'), True):
                pass
                l_1_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-originate', ))
                _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map')):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map'), ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'always'), True):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' always', ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                yield '   '
                yield str((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'send_community'), 'all'):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' send-community\n'
            elif t_8(environment.getattr(l_1_neighbor, 'send_community')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' send-community '
                yield str(environment.getattr(l_1_neighbor, 'send_community'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'maximum_routes')):
                pass
                l_1_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' maximum-routes ', environment.getattr(l_1_neighbor, 'maximum_routes'), ))
                _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_8(environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit')):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-limit ', environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit'), ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_8(environment.getattr(l_1_neighbor, 'maximum_routes_warning_only'), True):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-only', ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                yield '   '
                yield str((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'link_bandwidth'), 'enabled'), True):
                pass
                l_1_link_bandwidth_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' link-bandwidth', ))
                _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'link_bandwidth'), 'default')):
                    pass
                    l_1_link_bandwidth_cli = str_join(((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli), ' default ', environment.getattr(environment.getattr(l_1_neighbor, 'link_bandwidth'), 'default'), ))
                    _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                yield '   '
                yield str((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli))
                yield '\n'
        l_1_neighbor = l_1_remove_private_as_cli = l_1_remove_private_as_ingress_cli = l_1_allowas_in_cli = l_1_neighbor_rib_in_pre_policy_retain_cli = l_1_hide_passwords = l_1_default_originate_cli = l_1_maximum_routes_cli = l_1_link_bandwidth_cli = missing
        for l_1_aggregate_address in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'aggregate_addresses'), 'prefix'):
            l_1_aggregate_address_cli = missing
            _loop_vars = {}
            pass
            l_1_aggregate_address_cli = str_join(('aggregate-address ', environment.getattr(l_1_aggregate_address, 'prefix'), ))
            _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'as_set'), True):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' as-set', ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'advertise_map')):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' advertise-map ', environment.getattr(l_1_aggregate_address, 'advertise_map'), ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'supress_map')):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' supress-map ', environment.getattr(l_1_aggregate_address, 'supress_map'), ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'summary_only'), True):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' summary-only', ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'attribute_map')):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' attribute-map ', environment.getattr(l_1_aggregate_address, 'attribute_map'), ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'match_map')):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' match-map ', environment.getattr(l_1_aggregate_address, 'match_map'), ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'advertise_only'), True):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' advertise-only', ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            yield '   '
            yield str((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli))
            yield '\n'
        l_1_aggregate_address = l_1_aggregate_address_cli = missing
        for l_1_redistribute_route in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'redistribute_routes'), 'source_protocol'):
            l_1_redistribute_route_cli = resolve('redistribute_route_cli')
            _loop_vars = {}
            pass
            if t_8(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                pass
                l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'bgp'):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' leaked', ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif t_8(environment.getattr(l_1_redistribute_route, 'include_leaked')):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if t_8(environment.getattr(l_1_redistribute_route, 'route_map')):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                yield '   '
                yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                yield '\n'
        l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans')):
            pass
            l_0_bgp_vlans = environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans')
            context.vars['bgp_vlans'] = l_0_bgp_vlans
            context.exported_vars.add('bgp_vlans')
            for l_1_bgp_vlan in (undefined(name='bgp_vlans') if l_0_bgp_vlans is missing else l_0_bgp_vlans):
                _loop_vars = {}
                pass
                context.call(environment.getattr(l_1_bgp_vlan, 'update'), {'id': t_7(environment.getitem(l_1_bgp_vlan, 'id'))}, _loop_vars=_loop_vars)
            l_1_bgp_vlan = missing
            for l_1_vlan in t_6(environment, (undefined(name='bgp_vlans') if l_0_bgp_vlans is missing else l_0_bgp_vlans), attribute='id'):
                _loop_vars = {}
                pass
                yield '   !\n   vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield '\n'
                if t_8(environment.getattr(l_1_vlan, 'rd')):
                    pass
                    yield '      rd '
                    yield str(environment.getattr(l_1_vlan, 'rd'))
                    yield '\n'
                if (t_8(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'domain')) and t_8(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'rd'))):
                    pass
                    yield '      rd evpn domain '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'domain'))
                    yield ' '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'rd'))
                    yield '\n'
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'both')):
                    _loop_vars = {}
                    pass
                    yield '      route-target both '
                    yield str(l_2_route_target)
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import')):
                    _loop_vars = {}
                    pass
                    yield '      route-target import '
                    yield str(l_2_route_target)
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export')):
                    _loop_vars = {}
                    pass
                    yield '      route-target export '
                    yield str(l_2_route_target)
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_evpn_domains')):
                    _loop_vars = {}
                    pass
                    yield '      route-target import evpn domain '
                    yield str(environment.getattr(l_2_route_target, 'domain'))
                    yield ' '
                    yield str(environment.getattr(l_2_route_target, 'route_target'))
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export_evpn_domains')):
                    _loop_vars = {}
                    pass
                    yield '      route-target export evpn domain '
                    yield str(environment.getattr(l_2_route_target, 'domain'))
                    yield ' '
                    yield str(environment.getattr(l_2_route_target, 'route_target'))
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_export_evpn_domains')):
                    _loop_vars = {}
                    pass
                    yield '      route-target import export evpn domain '
                    yield str(environment.getattr(l_2_route_target, 'domain'))
                    yield ' '
                    yield str(environment.getattr(l_2_route_target, 'route_target'))
                    yield '\n'
                l_2_route_target = missing
                for l_2_redistribute_route in t_3(environment.getattr(l_1_vlan, 'redistribute_routes')):
                    _loop_vars = {}
                    pass
                    yield '      redistribute '
                    yield str(l_2_redistribute_route)
                    yield '\n'
                l_2_redistribute_route = missing
                for l_2_no_redistribute_route in t_3(environment.getattr(l_1_vlan, 'no_redistribute_routes')):
                    _loop_vars = {}
                    pass
                    yield '      no redistribute '
                    yield str(l_2_no_redistribute_route)
                    yield '\n'
                l_2_no_redistribute_route = missing
                if t_8(environment.getattr(l_1_vlan, 'eos_cli')):
                    pass
                    yield '      !\n      '
                    yield str(t_4(environment.getattr(l_1_vlan, 'eos_cli'), 6, False))
                    yield '\n'
            l_1_vlan = missing
        for l_1_vlan_aware_bundle in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlan_aware_bundles'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   vlan-aware-bundle '
            yield str(environment.getattr(l_1_vlan_aware_bundle, 'name'))
            yield '\n'
            if t_8(environment.getattr(l_1_vlan_aware_bundle, 'rd')):
                pass
                yield '      rd '
                yield str(environment.getattr(l_1_vlan_aware_bundle, 'rd'))
                yield '\n'
            if (t_8(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'domain')) and t_8(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'rd'))):
                pass
                yield '      rd evpn domain '
                yield str(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'domain'))
                yield ' '
                yield str(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'rd'))
                yield '\n'
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'both')):
                _loop_vars = {}
                pass
                yield '      route-target both '
                yield str(l_2_route_target)
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import')):
                _loop_vars = {}
                pass
                yield '      route-target import '
                yield str(l_2_route_target)
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export')):
                _loop_vars = {}
                pass
                yield '      route-target export '
                yield str(l_2_route_target)
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_evpn_domains')):
                _loop_vars = {}
                pass
                yield '      route-target import evpn domain '
                yield str(environment.getattr(l_2_route_target, 'domain'))
                yield ' '
                yield str(environment.getattr(l_2_route_target, 'route_target'))
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export_evpn_domains')):
                _loop_vars = {}
                pass
                yield '      route-target export evpn domain '
                yield str(environment.getattr(l_2_route_target, 'domain'))
                yield ' '
                yield str(environment.getattr(l_2_route_target, 'route_target'))
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_export_evpn_domains')):
                _loop_vars = {}
                pass
                yield '      route-target import export evpn domain '
                yield str(environment.getattr(l_2_route_target, 'domain'))
                yield ' '
                yield str(environment.getattr(l_2_route_target, 'route_target'))
                yield '\n'
            l_2_route_target = missing
            for l_2_redistribute_route in t_3(environment.getattr(l_1_vlan_aware_bundle, 'redistribute_routes')):
                _loop_vars = {}
                pass
                yield '      redistribute '
                yield str(l_2_redistribute_route)
                yield '\n'
            l_2_redistribute_route = missing
            for l_2_no_redistribute_route in t_3(environment.getattr(l_1_vlan_aware_bundle, 'no_redistribute_routes')):
                _loop_vars = {}
                pass
                yield '      no redistribute '
                yield str(l_2_no_redistribute_route)
                yield '\n'
            l_2_no_redistribute_route = missing
            yield '      vlan '
            yield str(environment.getattr(l_1_vlan_aware_bundle, 'vlan'))
            yield '\n'
            if t_8(environment.getattr(l_1_vlan_aware_bundle, 'eos_cli')):
                pass
                yield '      !\n      '
                yield str(t_4(environment.getattr(l_1_vlan_aware_bundle, 'eos_cli'), 6, False))
                yield '\n'
        l_1_vlan_aware_bundle = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws')):
            pass
            for l_1_vpws_service in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws'), 'name'):
                _loop_vars = {}
                pass
                yield '   !\n'
                if t_8(environment.getattr(l_1_vpws_service, 'name')):
                    pass
                    yield '   vpws '
                    yield str(environment.getattr(l_1_vpws_service, 'name'))
                    yield '\n'
                    if t_8(environment.getattr(l_1_vpws_service, 'rd')):
                        pass
                        yield '      rd '
                        yield str(environment.getattr(l_1_vpws_service, 'rd'))
                        yield '\n'
                    if t_8(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export')):
                        pass
                        yield '      route-target import export evpn '
                        yield str(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export'))
                        yield '\n'
                    if t_8(environment.getattr(l_1_vpws_service, 'mpls_control_word'), True):
                        pass
                        yield '      mpls control-word\n'
                    if t_8(environment.getattr(l_1_vpws_service, 'label_flow'), True):
                        pass
                        yield '      label flow\n'
                    if t_8(environment.getattr(l_1_vpws_service, 'mtu')):
                        pass
                        yield '      mtu '
                        yield str(environment.getattr(l_1_vpws_service, 'mtu'))
                        yield '\n'
                    for l_2_pw in t_3(environment.getattr(l_1_vpws_service, 'pseudowires'), 'name'):
                        _loop_vars = {}
                        pass
                        if ((t_8(environment.getattr(l_2_pw, 'name')) and t_8(environment.getattr(l_2_pw, 'id_local'))) and t_8(environment.getattr(l_2_pw, 'id_remote'))):
                            pass
                            yield '      !\n      pseudowire '
                            yield str(environment.getattr(l_2_pw, 'name'))
                            yield '\n         evpn vpws id local '
                            yield str(environment.getattr(l_2_pw, 'id_local'))
                            yield ' remote '
                            yield str(environment.getattr(l_2_pw, 'id_remote'))
                            yield '\n'
                    l_2_pw = missing
            l_1_vpws_service = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn')):
            pass
            yield '   !\n   address-family evpn\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_unchanged'), True):
                pass
                yield '      bgp next-hop-unchanged\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'enabled'), False):
                pass
                yield '      no host-flap detection\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'enabled'), True):
                pass
                l_0_hostflap_detection_cli = ''
                context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                context.exported_vars.add('hostflap_detection_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window')):
                    pass
                    l_0_hostflap_detection_cli = str_join(((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli), ' window ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window'), ))
                    context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                    context.exported_vars.add('hostflap_detection_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'threshold')):
                    pass
                    l_0_hostflap_detection_cli = str_join(((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli), ' threshold ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'threshold'), ))
                    context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                    context.exported_vars.add('hostflap_detection_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout')):
                    pass
                    l_0_hostflap_detection_cli = str_join(((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli), ' expiry timeout ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout'), ' seconds', ))
                    context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                    context.exported_vars.add('hostflap_detection_cli')
                if ((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli) != ''):
                    pass
                    yield '      host-flap detection'
                    yield str((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli))
                    yield '\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'domain_identifier')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'domain_identifier'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'encapsulation'), 'mpls'):
                pass
                l_0_evpn_neighbor_default_encap_cli = 'neighbor default encapsulation mpls'
                context.vars['evpn_neighbor_default_encap_cli'] = l_0_evpn_neighbor_default_encap_cli
                context.exported_vars.add('evpn_neighbor_default_encap_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_source_interface')):
                    pass
                    l_0_evpn_neighbor_default_encap_cli = str_join(((undefined(name='evpn_neighbor_default_encap_cli') if l_0_evpn_neighbor_default_encap_cli is missing else l_0_evpn_neighbor_default_encap_cli), ' next-hop-self source-interface ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_source_interface'), ))
                    context.vars['evpn_neighbor_default_encap_cli'] = l_0_evpn_neighbor_default_encap_cli
                    context.exported_vars.add('evpn_neighbor_default_encap_cli')
                yield '      '
                yield str((undefined(name='evpn_neighbor_default_encap_cli') if l_0_evpn_neighbor_default_encap_cli is missing else l_0_evpn_neighbor_default_encap_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_mpls_resolution_ribs')):
                pass
                l_0_evpn_mpls_resolution_ribs = []
                context.vars['evpn_mpls_resolution_ribs'] = l_0_evpn_mpls_resolution_ribs
                context.exported_vars.add('evpn_mpls_resolution_ribs')
                for l_1_rib in environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_mpls_resolution_ribs'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib-colored'):
                        pass
                        context.call(environment.getattr((undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), 'append'), 'tunnel-rib-colored system-colored-tunnel-rib', _loop_vars=_loop_vars)
                    elif (t_8(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib') and t_8(environment.getattr(l_1_rib, 'rib_name'))):
                        pass
                        context.call(environment.getattr((undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), 'append'), str_join(('tunnel-rib ', environment.getattr(l_1_rib, 'rib_name'), )), _loop_vars=_loop_vars)
                    elif t_8(environment.getattr(l_1_rib, 'rib_type')):
                        pass
                        context.call(environment.getattr((undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), 'append'), environment.getattr(l_1_rib, 'rib_type'), _loop_vars=_loop_vars)
                l_1_rib = missing
                if (undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs):
                    pass
                    yield '      next-hop mpls resolution ribs '
                    yield str(t_5(context.eval_ctx, (undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), ' '))
                    yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'any'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'domain_remote'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' domain remote\n'
                if t_8(environment.getattr(l_1_peer_group, 'encapsulation')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' encapsulation '
                    yield str(environment.getattr(l_1_peer_group, 'encapsulation'))
                    yield '\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop'), 'resolution_disabled'), True):
                pass
                yield '      next-hop resolution disabled\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'enable'), True):
                pass
                l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli = 'neighbor default next-hop-self received-evpn-routes route-type ip-prefix'
                context.vars['evpn_neighbor_default_nhs_received_evpn_routes_cli'] = l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli
                context.exported_vars.add('evpn_neighbor_default_nhs_received_evpn_routes_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'inter_domain'), True):
                    pass
                    l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli = str_join(((undefined(name='evpn_neighbor_default_nhs_received_evpn_routes_cli') if l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli is missing else l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli), ' inter-domain', ))
                    context.vars['evpn_neighbor_default_nhs_received_evpn_routes_cli'] = l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli
                    context.exported_vars.add('evpn_neighbor_default_nhs_received_evpn_routes_cli')
                yield '      '
                yield str((undefined(name='evpn_neighbor_default_nhs_received_evpn_routes_cli') if l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli is missing else l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '      route import match-failure action discard\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_ethernet_segment_ip_mass_withdraw'), True):
                pass
                yield '      route import ethernet-segment ip mass-withdraw\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'export_ethernet_segment_ip_mass_withdraw'), True):
                pass
                yield '      route export ethernet-segment ip mass-withdraw\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4')):
            pass
            yield '   !\n   address-family flow-spec ipv4\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6')):
            pass
            yield '   !\n   address-family flow-spec ipv6\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_rtc')):
            pass
            yield '   !\n   address-family rt-membership\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_rtc'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_9(environment.getattr(l_1_peer_group, 'default_route_target')):
                    pass
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route_target'), 'only'), True):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' default-route-target only\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' default-route-target\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'default_route_target'), 'encoding_origin_as_omit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' default-route-target encoding origin-as omit\n'
            l_1_peer_group = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4')):
            pass
            yield '   !\n   address-family ipv4\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'peer_groups'), 'name'):
                l_1_neighbor_default_originate_cli = resolve('neighbor_default_originate_cli')
                l_1_nexthop_v6_cli = resolve('nexthop_v6_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'default_originate')):
                    pass
                    l_1_neighbor_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-originate', ))
                    _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map')):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map'), ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'always'), True):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' always', ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'next_hop'), 'address_family_ipv6'), 'enabled'), True):
                    pass
                    l_1_nexthop_v6_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' next-hop address-family ipv6', ))
                    _loop_vars['nexthop_v6_cli'] = l_1_nexthop_v6_cli
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'next_hop'), 'address_family_ipv6'), 'originate'), True):
                        pass
                        l_1_nexthop_v6_cli = str_join(((undefined(name='nexthop_v6_cli') if l_1_nexthop_v6_cli is missing else l_1_nexthop_v6_cli), ' originate', ))
                        _loop_vars['nexthop_v6_cli'] = l_1_nexthop_v6_cli
                    yield '      '
                    yield str((undefined(name='nexthop_v6_cli') if l_1_nexthop_v6_cli is missing else l_1_nexthop_v6_cli))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'next_hop'), 'address_family_ipv6_originate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' next-hop address-family ipv6 originate\n'
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = l_1_neighbor_default_originate_cli = l_1_nexthop_v6_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'neighbors'), 'ip_address'):
                l_1_neighbor_default_originate_cli = resolve('neighbor_default_originate_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'default_originate')):
                    pass
                    l_1_neighbor_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-originate', ))
                    _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map')):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map'), ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'always'), True):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' always', ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli))
                    yield '\n'
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = l_1_neighbor_default_originate_cli = missing
            for l_1_network in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'networks'), 'prefix'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_network, 'route_map')):
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_network, 'route_map'))
                    yield '\n'
                else:
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield '\n'
            l_1_network = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast')):
            pass
            yield '   !\n   address-family ipv4 multicast\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
            for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'redistribute_routes'), 'source_protocol'):
                l_1_redistribute_route_cli = resolve('redistribute_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_8(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
            l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te')):
            pass
            yield '   !\n   address-family ipv4 sr-te\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6')):
            pass
            yield '   !\n   address-family ipv6\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
            for l_1_network in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'networks'), 'prefix'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_network, 'route_map')):
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_network, 'route_map'))
                    yield '\n'
                else:
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield '\n'
            l_1_network = missing
            for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'redistribute_routes'), 'source_protocol'):
                l_1_redistribute_route_cli = resolve('redistribute_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'bgp'):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif t_8(environment.getattr(l_1_redistribute_route, 'include_leaked')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_8(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
            l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast')):
            pass
            yield '   !\n   address-family ipv6 multicast\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
            for l_1_network in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'networks'), 'prefix'):
                l_1_network_cli = missing
                _loop_vars = {}
                pass
                l_1_network_cli = str_join(('network ', environment.getattr(l_1_network, 'prefix'), ))
                _loop_vars['network_cli'] = l_1_network_cli
                if t_8(environment.getattr(l_1_network, 'route_map')):
                    pass
                    l_1_network_cli = str_join(((undefined(name='network_cli') if l_1_network_cli is missing else l_1_network_cli), ' route-map ', environment.getattr(l_1_network, 'route_map'), ))
                    _loop_vars['network_cli'] = l_1_network_cli
                yield '      '
                yield str((undefined(name='network_cli') if l_1_network_cli is missing else l_1_network_cli))
                yield '\n'
            l_1_network = l_1_network_cli = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te')):
            pass
            yield '   !\n   address-family ipv6 sr-te\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state')):
            pass
            yield '   !\n   address-family link-state\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_out_action'))
                    yield '\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_out_action'))
                    yield '\n'
            l_1_neighbor = missing
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection')):
                pass
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'producer'), True):
                    pass
                    yield '      path-selection\n'
                if (t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'consumer'), True) or t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'propagator'), True)):
                    pass
                    l_0_path_selection_roles = 'path-selection role'
                    context.vars['path_selection_roles'] = l_0_path_selection_roles
                    context.exported_vars.add('path_selection_roles')
                    if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'consumer'), True):
                        pass
                        l_0_path_selection_roles = str_join(((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), ' consumer', ))
                        context.vars['path_selection_roles'] = l_0_path_selection_roles
                        context.exported_vars.add('path_selection_roles')
                    if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'propagator'), True):
                        pass
                        l_0_path_selection_roles = str_join(((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), ' propagator', ))
                        context.vars['path_selection_roles'] = l_0_path_selection_roles
                        context.exported_vars.add('path_selection_roles')
                    yield '      '
                    yield str((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles))
                    yield '\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection')):
            pass
            yield '   !\n   address-family path-selection\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'any'), True):
                pass
                yield '      bgp additional-paths send any\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'backup'), True):
                pass
                yield '      bgp additional-paths send backup\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'ecmp'), True):
                pass
                yield '      bgp additional-paths send ecmp\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit')):
                pass
                yield '      bgp additional-paths send ecmp limit '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit'))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'limit')):
                pass
                yield '      bgp additional-paths send limit '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'limit'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4')):
            pass
            yield '   !\n   address-family vpn-ipv4\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'domain_identifier')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'domain_identifier'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface')):
                pass
                yield '      neighbor default encapsulation mpls next-hop-self source-interface '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '      route import match-failure action discard\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6')):
            pass
            yield '   !\n   address-family vpn-ipv6\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'domain_identifier')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'domain_identifier'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface')):
                pass
                yield '      neighbor default encapsulation mpls next-hop-self source-interface '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '      route import match-failure action discard\n'
        for l_1_vrf in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
            l_1_tmp_vrf_neighbor_prefix_list_in = l_1_tmp_vrf_neighbor_prefix_list_out = missing
            _loop_vars = {}
            pass
            yield '   !\n   vrf '
            yield str(environment.getattr(l_1_vrf, 'name'))
            yield '\n'
            if t_8(environment.getattr(l_1_vrf, 'rd')):
                pass
                yield '      rd '
                yield str(environment.getattr(l_1_vrf, 'rd'))
                yield '\n'
            if t_8(environment.getattr(l_1_vrf, 'evpn_multicast'), True):
                pass
                yield '      evpn multicast\n'
                if (t_8(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4')) and t_8(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4'), 'transit'), True)):
                    pass
                    yield '         address-family ipv4\n'
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4'), 'transit'), True):
                        pass
                        yield '            transit\n'
            if t_8(environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'import')):
                pass
                for l_2_address_family in environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'import'):
                    _loop_vars = {}
                    pass
                    for l_3_route_target in environment.getattr(l_2_address_family, 'route_targets'):
                        _loop_vars = {}
                        pass
                        yield '      route-target import '
                        yield str(environment.getattr(l_2_address_family, 'address_family'))
                        yield ' '
                        yield str(l_3_route_target)
                        yield '\n'
                    l_3_route_target = missing
                    if t_8(environment.getattr(l_2_address_family, 'route_map')):
                        pass
                        yield '      route-target import '
                        yield str(environment.getattr(l_2_address_family, 'address_family'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_address_family, 'route_map'))
                        yield '\n'
                l_2_address_family = missing
            if t_8(environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'export')):
                pass
                for l_2_address_family in environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'export'):
                    _loop_vars = {}
                    pass
                    for l_3_route_target in environment.getattr(l_2_address_family, 'route_targets'):
                        _loop_vars = {}
                        pass
                        yield '      route-target export '
                        yield str(environment.getattr(l_2_address_family, 'address_family'))
                        yield ' '
                        yield str(l_3_route_target)
                        yield '\n'
                    l_3_route_target = missing
                    if t_8(environment.getattr(l_2_address_family, 'route_map')):
                        pass
                        yield '      route-target export '
                        yield str(environment.getattr(l_2_address_family, 'address_family'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_address_family, 'route_map'))
                        yield '\n'
                l_2_address_family = missing
            if t_8(environment.getattr(l_1_vrf, 'router_id')):
                pass
                yield '      router-id '
                yield str(environment.getattr(l_1_vrf, 'router_id'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_vrf, 'updates'), 'wait_for_convergence'), True):
                pass
                yield '      update wait-for-convergence\n'
            if t_8(environment.getattr(environment.getattr(l_1_vrf, 'updates'), 'wait_install'), True):
                pass
                yield '      update wait-install\n'
            if t_8(environment.getattr(l_1_vrf, 'timers')):
                pass
                yield '      timers bgp '
                yield str(environment.getattr(l_1_vrf, 'timers'))
                yield '\n'
            if t_8(environment.getattr(l_1_vrf, 'listen_ranges')):
                pass
                def t_12(fiter):
                    for l_2_listen_range in fiter:
                        if ((t_8(environment.getattr(l_2_listen_range, 'peer_group')) and t_8(environment.getattr(l_2_listen_range, 'prefix'))) and (t_8(environment.getattr(l_2_listen_range, 'peer_filter')) or t_8(environment.getattr(l_2_listen_range, 'remote_as')))):
                            yield l_2_listen_range
                for l_2_listen_range in t_12(t_3(environment.getattr(l_1_vrf, 'listen_ranges'), 'peer_group')):
                    l_2_listen_range_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_listen_range_cli = str_join(('bgp listen range ', environment.getattr(l_2_listen_range, 'prefix'), ))
                    _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    if t_8(environment.getattr(l_2_listen_range, 'peer_id_include_router_id'), True):
                        pass
                        l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' peer-id include router-id', ))
                        _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' peer-group ', environment.getattr(l_2_listen_range, 'peer_group'), ))
                    _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    if t_8(environment.getattr(l_2_listen_range, 'peer_filter')):
                        pass
                        l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' peer-filter ', environment.getattr(l_2_listen_range, 'peer_filter'), ))
                        _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    elif t_8(environment.getattr(l_2_listen_range, 'remote_as')):
                        pass
                        l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' remote-as ', environment.getattr(l_2_listen_range, 'remote_as'), ))
                        _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    yield '      '
                    yield str((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli))
                    yield '\n'
                l_2_listen_range = l_2_listen_range_cli = missing
            for l_2_neighbor_interface in t_3(environment.getattr(l_1_vrf, 'neighbor_interfaces'), 'name'):
                _loop_vars = {}
                pass
                if (t_8(environment.getattr(l_2_neighbor_interface, 'peer_group')) and t_8(environment.getattr(l_2_neighbor_interface, 'remote_as'))):
                    pass
                    yield '      neighbor interface '
                    yield str(environment.getattr(l_2_neighbor_interface, 'name'))
                    yield ' peer-group '
                    yield str(environment.getattr(l_2_neighbor_interface, 'peer_group'))
                    yield ' remote-as '
                    yield str(environment.getattr(l_2_neighbor_interface, 'remote_as'))
                    yield '\n'
                elif (t_8(environment.getattr(l_2_neighbor_interface, 'peer_group')) and t_8(environment.getattr(l_2_neighbor_interface, 'peer_filter'))):
                    pass
                    yield '      neighbor interface '
                    yield str(environment.getattr(l_2_neighbor_interface, 'name'))
                    yield ' peer-group '
                    yield str(environment.getattr(l_2_neighbor_interface, 'peer_group'))
                    yield ' peer-filter '
                    yield str(environment.getattr(l_2_neighbor_interface, 'peer_filter'))
                    yield '\n'
            l_2_neighbor_interface = missing
            l_1_tmp_vrf_neighbor_prefix_list_in = {}
            _loop_vars['tmp_vrf_neighbor_prefix_list_in'] = l_1_tmp_vrf_neighbor_prefix_list_in
            l_1_tmp_vrf_neighbor_prefix_list_out = {}
            _loop_vars['tmp_vrf_neighbor_prefix_list_out'] = l_1_tmp_vrf_neighbor_prefix_list_out
            for l_2_neighbor in t_3(environment.getattr(l_1_vrf, 'neighbors'), 'ip_address'):
                l_2_remove_private_as_cli = resolve('remove_private_as_cli')
                l_2_remove_private_as_ingress_cli = resolve('remove_private_as_ingress_cli')
                l_2_hide_passwords = resolve('hide_passwords')
                l_2_neighbor_ebgp_multihop_cli = resolve('neighbor_ebgp_multihop_cli')
                l_2_allowas_in_cli = resolve('allowas_in_cli')
                l_2_neighbor_rib_in_pre_policy_retain_cli = resolve('neighbor_rib_in_pre_policy_retain_cli')
                l_2_maximum_routes_cli = resolve('maximum_routes_cli')
                l_2_neighbor_default_originate_cli = resolve('neighbor_default_originate_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_2_neighbor, 'remote_as')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' remote-as '
                    yield str(environment.getattr(l_2_neighbor, 'remote_as'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'peer_group')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' peer group '
                    yield str(environment.getattr(l_2_neighbor, 'peer_group'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'enabled'), True):
                    pass
                    l_2_remove_private_as_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' remove-private-as', ))
                    _loop_vars['remove_private_as_cli'] = l_2_remove_private_as_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'all'), True):
                        pass
                        l_2_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_2_remove_private_as_cli is missing else l_2_remove_private_as_cli), ' all', ))
                        _loop_vars['remove_private_as_cli'] = l_2_remove_private_as_cli
                        if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'replace_as'), True):
                            pass
                            l_2_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_2_remove_private_as_cli is missing else l_2_remove_private_as_cli), ' replace-as', ))
                            _loop_vars['remove_private_as_cli'] = l_2_remove_private_as_cli
                    yield '      '
                    yield str((undefined(name='remove_private_as_cli') if l_2_remove_private_as_cli is missing else l_2_remove_private_as_cli))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'enabled'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' remove-private-as\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as_ingress'), 'enabled'), True):
                    pass
                    l_2_remove_private_as_ingress_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' remove-private-as ingress', ))
                    _loop_vars['remove_private_as_ingress_cli'] = l_2_remove_private_as_ingress_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as_ingress'), 'replace_as'), True):
                        pass
                        l_2_remove_private_as_ingress_cli = str_join(((undefined(name='remove_private_as_ingress_cli') if l_2_remove_private_as_ingress_cli is missing else l_2_remove_private_as_ingress_cli), ' replace-as', ))
                        _loop_vars['remove_private_as_ingress_cli'] = l_2_remove_private_as_ingress_cli
                    yield '      '
                    yield str((undefined(name='remove_private_as_ingress_cli') if l_2_remove_private_as_ingress_cli is missing else l_2_remove_private_as_ingress_cli))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as_ingress'), 'enabled'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' remove-private-as ingress\n'
                if t_8(environment.getattr(l_2_neighbor, 'password')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' password 7 '
                    yield str(t_2(environment.getattr(l_2_neighbor, 'password'), (undefined(name='hide_passwords') if l_2_hide_passwords is missing else l_2_hide_passwords)))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'passive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' passive\n'
                if t_8(environment.getattr(l_2_neighbor, 'weight')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' weight '
                    yield str(environment.getattr(l_2_neighbor, 'weight'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'as_path'), 'remote_as_replace_out'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' as-path remote-as replace out\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'as_path'), 'prepend_own_disabled'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' as-path prepend-own disabled\n'
                if t_8(environment.getattr(l_2_neighbor, 'local_as')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' local-as '
                    yield str(environment.getattr(l_2_neighbor, 'local_as'))
                    yield ' no-prepend replace-as\n'
                if t_8(environment.getattr(l_2_neighbor, 'description')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' description '
                    yield str(environment.getattr(l_2_neighbor, 'description'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'ebgp_multihop')):
                    pass
                    l_2_neighbor_ebgp_multihop_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' ebgp-multihop', ))
                    _loop_vars['neighbor_ebgp_multihop_cli'] = l_2_neighbor_ebgp_multihop_cli
                    if t_10(environment.getattr(l_2_neighbor, 'ebgp_multihop')):
                        pass
                        l_2_neighbor_ebgp_multihop_cli = str_join(((undefined(name='neighbor_ebgp_multihop_cli') if l_2_neighbor_ebgp_multihop_cli is missing else l_2_neighbor_ebgp_multihop_cli), ' ', environment.getattr(l_2_neighbor, 'ebgp_multihop'), ))
                        _loop_vars['neighbor_ebgp_multihop_cli'] = l_2_neighbor_ebgp_multihop_cli
                    yield '      '
                    yield str((undefined(name='neighbor_ebgp_multihop_cli') if l_2_neighbor_ebgp_multihop_cli is missing else l_2_neighbor_ebgp_multihop_cli))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'next_hop_self'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' next-hop-self\n'
                if t_8(environment.getattr(l_2_neighbor, 'bfd'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' bfd\n'
                    if ((t_8(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'interval')) and t_8(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'min_rx'))) and t_8(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'multiplier'))):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' bfd interval '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'interval'))
                        yield ' min-rx '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'min_rx'))
                        yield ' multiplier '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'multiplier'))
                        yield '\n'
                elif (t_8(environment.getattr(l_2_neighbor, 'bfd'), False) and t_8(environment.getattr(l_2_neighbor, 'peer_group'))):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' bfd\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'enabled'), True):
                    pass
                    l_2_allowas_in_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' allowas-in', ))
                    _loop_vars['allowas_in_cli'] = l_2_allowas_in_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times')):
                        pass
                        l_2_allowas_in_cli = str_join(((undefined(name='allowas_in_cli') if l_2_allowas_in_cli is missing else l_2_allowas_in_cli), ' ', environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times'), ))
                        _loop_vars['allowas_in_cli'] = l_2_allowas_in_cli
                    yield '      '
                    yield str((undefined(name='allowas_in_cli') if l_2_allowas_in_cli is missing else l_2_allowas_in_cli))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True):
                    pass
                    l_2_neighbor_rib_in_pre_policy_retain_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_2_neighbor_rib_in_pre_policy_retain_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'all'), True):
                        pass
                        l_2_neighbor_rib_in_pre_policy_retain_cli = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_2_neighbor_rib_in_pre_policy_retain_cli is missing else l_2_neighbor_rib_in_pre_policy_retain_cli), ' all', ))
                        _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_2_neighbor_rib_in_pre_policy_retain_cli
                    yield '      '
                    yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_2_neighbor_rib_in_pre_policy_retain_cli is missing else l_2_neighbor_rib_in_pre_policy_retain_cli))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), False):
                    pass
                    l_2_neighbor_rib_in_pre_policy_retain_cli = str_join(('no neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_2_neighbor_rib_in_pre_policy_retain_cli
                    yield '      '
                    yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_2_neighbor_rib_in_pre_policy_retain_cli is missing else l_2_neighbor_rib_in_pre_policy_retain_cli))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'timers')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' timers '
                    yield str(environment.getattr(l_2_neighbor, 'timers'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'shutdown'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' shutdown\n'
                if t_8(environment.getattr(l_2_neighbor, 'send_community'), 'all'):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' send-community\n'
                elif t_8(environment.getattr(l_2_neighbor, 'send_community')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' send-community '
                    yield str(environment.getattr(l_2_neighbor, 'send_community'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'route_reflector_client'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-reflector-client\n'
                elif t_8(environment.getattr(l_2_neighbor, 'route_reflector_client'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-reflector-client\n'
                if t_8(environment.getattr(l_2_neighbor, 'maximum_routes')):
                    pass
                    l_2_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' maximum-routes ', environment.getattr(l_2_neighbor, 'maximum_routes'), ))
                    _loop_vars['maximum_routes_cli'] = l_2_maximum_routes_cli
                    if t_8(environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit')):
                        pass
                        l_2_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_2_maximum_routes_cli is missing else l_2_maximum_routes_cli), ' warning-limit ', environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit'), ))
                        _loop_vars['maximum_routes_cli'] = l_2_maximum_routes_cli
                    if t_8(environment.getattr(l_2_neighbor, 'maximum_routes_warning_only'), True):
                        pass
                        l_2_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_2_maximum_routes_cli is missing else l_2_maximum_routes_cli), ' warning-only', ))
                        _loop_vars['maximum_routes_cli'] = l_2_maximum_routes_cli
                    yield '      '
                    yield str((undefined(name='maximum_routes_cli') if l_2_maximum_routes_cli is missing else l_2_maximum_routes_cli))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'default_originate')):
                    pass
                    l_2_neighbor_default_originate_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' default-originate', ))
                    _loop_vars['neighbor_default_originate_cli'] = l_2_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'default_originate'), 'route_map')):
                        pass
                        l_2_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_2_neighbor_default_originate_cli is missing else l_2_neighbor_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_2_neighbor, 'default_originate'), 'route_map'), ))
                        _loop_vars['neighbor_default_originate_cli'] = l_2_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'default_originate'), 'always'), True):
                        pass
                        l_2_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_2_neighbor_default_originate_cli is missing else l_2_neighbor_default_originate_cli), ' always', ))
                        _loop_vars['neighbor_default_originate_cli'] = l_2_neighbor_default_originate_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_originate_cli') if l_2_neighbor_default_originate_cli is missing else l_2_neighbor_default_originate_cli))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'update_source')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' update-source '
                    yield str(environment.getattr(l_2_neighbor, 'update_source'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_2_neighbor, 'prefix_list_in')):
                    pass
                    context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), 'update'), {environment.getattr(l_2_neighbor, 'ip_address'): environment.getattr(l_2_neighbor, 'prefix_list_in')}, _loop_vars=_loop_vars)
                if t_8(environment.getattr(l_2_neighbor, 'prefix_list_out')):
                    pass
                    context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), 'update'), {environment.getattr(l_2_neighbor, 'ip_address'): environment.getattr(l_2_neighbor, 'prefix_list_out')}, _loop_vars=_loop_vars)
            l_2_neighbor = l_2_remove_private_as_cli = l_2_remove_private_as_ingress_cli = l_2_hide_passwords = l_2_neighbor_ebgp_multihop_cli = l_2_allowas_in_cli = l_2_neighbor_rib_in_pre_policy_retain_cli = l_2_maximum_routes_cli = l_2_neighbor_default_originate_cli = missing
            for l_2_network in t_3(environment.getattr(l_1_vrf, 'networks'), 'prefix'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_2_network, 'route_map')):
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_2_network, 'prefix'))
                    yield ' route-map '
                    yield str(environment.getattr(l_2_network, 'route_map'))
                    yield '\n'
                else:
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_2_network, 'prefix'))
                    yield '\n'
            l_2_network = missing
            for l_2_aggregate_address in t_3(environment.getattr(l_1_vrf, 'aggregate_addresses'), 'prefix'):
                l_2_aggregate_address_cli = missing
                _loop_vars = {}
                pass
                l_2_aggregate_address_cli = str_join(('aggregate-address ', environment.getattr(l_2_aggregate_address, 'prefix'), ))
                _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'as_set'), True):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' as-set', ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'advertise_map')):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' advertise-map ', environment.getattr(l_2_aggregate_address, 'advertise_map'), ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'supress_map')):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' supress-map ', environment.getattr(l_2_aggregate_address, 'supress_map'), ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'summary_only'), True):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' summary-only', ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'attribute_map')):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' attribute-map ', environment.getattr(l_2_aggregate_address, 'attribute_map'), ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'match_map')):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' match-map ', environment.getattr(l_2_aggregate_address, 'match_map'), ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'advertise_only'), True):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' advertise-only', ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                yield '      '
                yield str((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli))
                yield '\n'
            l_2_aggregate_address = l_2_aggregate_address_cli = missing
            for l_2_redistribute_route in t_3(environment.getattr(l_1_vrf, 'redistribute_routes'), 'source_protocol'):
                l_2_redistribute_route_cli = resolve('redistribute_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_2_redistribute_route, 'source_protocol')):
                    pass
                    l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    if (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'bgp'):
                        pass
                        l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    elif t_8(environment.getattr(l_2_redistribute_route, 'include_leaked')):
                        pass
                        l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    if t_8(environment.getattr(l_2_redistribute_route, 'route_map')):
                        pass
                        l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                    yield '\n'
            l_2_redistribute_route = l_2_redistribute_route_cli = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4')):
                pass
                yield '      !\n      address-family flow-spec ipv4\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                l_2_neighbor = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6')):
                pass
                yield '      !\n      address-family flow-spec ipv6\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                l_2_neighbor = missing
            if ((t_8(environment.getattr(l_1_vrf, 'address_family_ipv4')) or (undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in)) or (undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out)):
                pass
                yield '      !\n      address-family ipv4\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'install'), True):
                    pass
                    yield '         bgp additional-paths install\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'install_ecmp_primary'), True):
                    pass
                    yield '         bgp additional-paths install ecmp-primary\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '         bgp additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '         bgp additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '         bgp additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '         bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '         bgp additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'neighbors'), 'ip_address'):
                    l_2_ipv6_originate_cli = resolve('ipv6_originate_cli')
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                    if t_8(environment.getattr(l_2_neighbor, 'prefix_list_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_in'))
                        yield ' in\n'
                        if t_8(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), environment.getattr(l_2_neighbor, 'ip_address'))):
                            pass
                            context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), 'pop'), environment.getattr(l_2_neighbor, 'ip_address'), _loop_vars=_loop_vars)
                    elif t_8(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), environment.getattr(l_2_neighbor, 'ip_address'))):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), 'pop'), environment.getattr(l_2_neighbor, 'ip_address'), _loop_vars=_loop_vars))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'prefix_list_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_out'))
                        yield ' out\n'
                        if t_8(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), environment.getattr(l_2_neighbor, 'ip_address'))):
                            pass
                            context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), 'pop'), environment.getattr(l_2_neighbor, 'ip_address'), _loop_vars=_loop_vars)
                    elif t_8(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), environment.getattr(l_2_neighbor, 'ip_address'))):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), 'pop'), environment.getattr(l_2_neighbor, 'ip_address'), _loop_vars=_loop_vars))
                        yield ' out\n'
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'enabled')):
                        pass
                        if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'enabled'), True):
                            pass
                            l_2_ipv6_originate_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' next-hop address-family ipv6', ))
                            _loop_vars['ipv6_originate_cli'] = l_2_ipv6_originate_cli
                            if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'originate'), True):
                                pass
                                l_2_ipv6_originate_cli = str_join(((undefined(name='ipv6_originate_cli') if l_2_ipv6_originate_cli is missing else l_2_ipv6_originate_cli), ' originate', ))
                                _loop_vars['ipv6_originate_cli'] = l_2_ipv6_originate_cli
                        elif t_8(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'enabled'), False):
                            pass
                            l_2_ipv6_originate_cli = str_join(('no neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' next-hop address-family ipv6', ))
                            _loop_vars['ipv6_originate_cli'] = l_2_ipv6_originate_cli
                        yield '         '
                        yield str((undefined(name='ipv6_originate_cli') if l_2_ipv6_originate_cli is missing else l_2_ipv6_originate_cli))
                        yield '\n'
                l_2_neighbor = l_2_ipv6_originate_cli = missing
                for l_2_tmp_neighbor_ip in t_3((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in)):
                    _loop_vars = {}
                    pass
                    yield '         neighbor '
                    yield str(l_2_tmp_neighbor_ip)
                    yield ' prefix-list '
                    yield str(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), l_2_tmp_neighbor_ip))
                    yield ' in\n'
                l_2_tmp_neighbor_ip = missing
                for l_2_tmp_neighbor_ip in t_3((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out)):
                    _loop_vars = {}
                    pass
                    yield '         neighbor '
                    yield str(l_2_tmp_neighbor_ip)
                    yield ' prefix-list '
                    yield str(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), l_2_tmp_neighbor_ip))
                    yield ' out\n'
                l_2_tmp_neighbor_ip = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_8(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast')):
                pass
                yield '      !\n      address-family ipv4 multicast\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                l_2_neighbor = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_8(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_ipv6')):
                pass
                yield '      !\n      address-family ipv6\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'install'), True):
                    pass
                    yield '         bgp additional-paths install\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'install_ecmp_primary'), True):
                    pass
                    yield '         bgp additional-paths install ecmp-primary\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '         bgp additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '         bgp additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '         bgp additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '         bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '         bgp additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                    if t_8(environment.getattr(l_2_neighbor, 'prefix_list_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'prefix_list_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_out'))
                        yield ' out\n'
                l_2_neighbor = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_8(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast')):
                pass
                yield '      !\n      address-family ipv6 multicast\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                l_2_neighbor = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_8(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
            for l_2_address_family in t_3(environment.getattr(l_1_vrf, 'address_families'), 'address_family'):
                _loop_vars = {}
                pass
                yield '      !\n      address-family '
                yield str(environment.getattr(l_2_address_family, 'address_family'))
                yield '\n'
                if t_8(environment.getattr(l_2_address_family, 'bgp')):
                    pass
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'missing_policy'), 'direction_in_action')):
                        pass
                        yield '         bgp missing-policy direction in action '
                        yield str(environment.getattr(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'missing_policy'), 'direction_in_action'))
                        yield '\n'
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'missing_policy'), 'direction_out_action')):
                        pass
                        yield '         bgp missing-policy direction out action '
                        yield str(environment.getattr(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'missing_policy'), 'direction_out_action'))
                        yield '\n'
                    for l_3_additional_path in t_3(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'additional_paths')):
                        _loop_vars = {}
                        pass
                        yield '         bgp additional-paths '
                        yield str(l_3_additional_path)
                        yield '\n'
                    l_3_additional_path = missing
                for l_3_peer_group in t_3(environment.getattr(l_2_address_family, 'peer_groups'), 'name'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_3_peer_group, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_peer_group, 'name'))
                        yield ' activate\n'
                    elif t_8(environment.getattr(l_3_peer_group, 'activate'), False):
                        pass
                        yield '         no neighbor '
                        yield str(environment.getattr(l_3_peer_group, 'name'))
                        yield ' activate\n'
                    if t_8(environment.getattr(environment.getattr(l_3_peer_group, 'next_hop'), 'address_family_ipv6_originate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_peer_group, 'name'))
                        yield ' next-hop address-family ipv6 originate\n'
                l_3_peer_group = missing
                for l_3_neighbor in t_3(environment.getattr(l_2_address_family, 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_3_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_3_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_3_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_3_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_3_neighbor, 'route_map_out'))
                        yield ' out\n'
                l_3_neighbor = missing
                for l_3_network in t_3(environment.getattr(l_2_address_family, 'networks'), 'prefix'):
                    l_3_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_3_network_cli = str_join(('network ', environment.getattr(l_3_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_3_network_cli
                    if t_8(environment.getattr(l_3_network, 'route_map')):
                        pass
                        l_3_network_cli = str_join(((undefined(name='network_cli') if l_3_network_cli is missing else l_3_network_cli), ' route-map ', environment.getattr(l_3_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_3_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_3_network_cli is missing else l_3_network_cli))
                    yield '\n'
                l_3_network = l_3_network_cli = missing
            l_2_address_family = missing
            if t_8(environment.getattr(l_1_vrf, 'eos_cli')):
                pass
                yield '      !\n      '
                yield str(t_4(environment.getattr(l_1_vrf, 'eos_cli'), 6, False))
                yield '\n'
        l_1_vrf = l_1_tmp_vrf_neighbor_prefix_list_in = l_1_tmp_vrf_neighbor_prefix_list_out = missing
        for l_1_session_tracker in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'session_trackers'), 'name'):
            _loop_vars = {}
            pass
            yield '   session tracker '
            yield str(environment.getattr(l_1_session_tracker, 'name'))
            yield '\n'
            if t_8(environment.getattr(l_1_session_tracker, 'recovery_delay')):
                pass
                yield '      recovery delay '
                yield str(environment.getattr(l_1_session_tracker, 'recovery_delay'))
                yield ' seconds\n'
        l_1_session_tracker = missing

blocks = {}
debug_info = '7=81&9=84&10=86&11=89&13=91&14=94&16=96&17=98&18=101&19=103&21=107&23=109&24=111&25=114&27=116&28=119&32=122&34=125&35=127&36=130&37=132&41=135&42=137&43=140&44=142&46=146&48=148&49=150&50=153&51=155&53=159&55=161&58=164&61=167&63=170&66=173&68=176&71=179&72=182&74=184&75=188&77=191&80=194&82=196&81=200&83=204&84=206&85=208&87=210&88=212&89=214&90=216&91=218&93=221&96=224&97=227&98=230&101=237&102=248&103=251&105=254&106=256&107=259&109=263&110=266&112=270&113=273&115=275&116=278&118=280&119=283&121=285&122=288&124=290&125=292&126=294&127=296&128=298&129=300&132=303&133=305&134=308&136=310&137=312&138=314&139=316&141=319&142=321&143=324&145=326&146=329&148=333&149=336&151=340&152=343&154=345&155=348&156=350&159=353&162=361&163=363&164=365&165=367&167=370&169=372&170=374&171=376&172=378&174=381&175=383&176=385&177=388&179=390&180=393&182=397&183=400&185=404&186=407&188=411&189=413&190=415&191=417&193=419&194=421&196=424&198=426&199=429&201=431&202=434&204=438&205=441&206=443&207=446&209=450&210=452&211=454&212=456&214=458&215=460&217=463&219=465&220=467&221=469&222=471&224=474&226=476&227=479&229=483&230=486&232=490&233=493&235=497&236=500&239=505&240=508&241=511&242=517&243=520&246=527&247=538&248=541&250=545&251=548&253=552&254=555&256=557&257=560&259=562&260=564&261=566&262=568&263=570&264=572&267=575&268=577&269=580&271=582&272=584&273=586&274=588&276=591&277=593&278=596&280=598&281=601&283=603&284=606&286=608&287=611&289=615&290=618&292=622&293=625&294=627&295=630&297=632&298=635&300=639&301=642&303=646&304=649&306=653&307=656&308=658&311=661&313=669&314=672&316=674&317=676&318=678&319=680&321=683&323=685&324=687&325=689&326=691&328=694&329=696&330=698&331=701&333=703&334=706&336=710&337=713&339=715&340=718&342=722&343=725&345=729&346=732&348=736&349=739&351=743&352=746&354=750&355=752&356=754&357=756&359=758&360=760&362=763&364=765&365=768&366=770&367=773&369=777&370=779&371=781&372=783&374=785&375=787&377=790&379=792&380=794&381=796&382=798&384=801&387=804&388=808&389=810&390=812&392=814&393=816&395=818&396=820&398=822&399=824&401=826&402=828&404=830&405=832&407=834&408=836&410=839&412=842&413=846&414=848&415=850&416=852&417=854&418=856&420=858&421=860&423=863&427=866&429=868&430=871&431=874&433=876&435=880&436=882&437=885&439=887&440=890&442=894&443=898&445=901&446=905&448=908&449=912&451=915&452=919&454=924&455=928&457=933&458=937&460=942&461=946&463=949&464=953&466=956&468=959&473=962&475=966&476=968&477=971&479=973&480=976&482=980&483=984&485=987&486=991&488=994&489=998&491=1001&492=1005&494=1010&495=1014&497=1019&498=1023&500=1028&501=1032&503=1035&504=1039&506=1043&507=1045&509=1048&513=1051&514=1053&516=1057&517=1060&518=1062&519=1065&521=1067&522=1070&524=1072&527=1075&530=1078&531=1081&533=1083&534=1086&536=1089&537=1091&545=1097&548=1100&551=1103&553=1106&554=1108&555=1111&556=1113&558=1116&559=1118&561=1121&562=1123&564=1126&565=1129&568=1131&569=1134&571=1136&572=1138&573=1141&574=1143&576=1147&578=1149&579=1151&580=1154&581=1157&582=1159&583=1160&584=1162&585=1163&586=1165&589=1167&590=1170&593=1172&594=1175&595=1178&597=1182&598=1185&600=1189&601=1192&602=1194&603=1197&605=1199&606=1202&608=1204&609=1207&610=1209&611=1212&612=1214&613=1217&614=1219&615=1222&616=1224&617=1227&618=1231&619=1234&621=1238&622=1241&624=1243&625=1246&628=1251&629=1254&630=1257&631=1259&632=1262&635=1265&638=1268&639=1270&640=1273&641=1275&643=1279&645=1281&648=1284&651=1287&656=1290&659=1293&660=1296&662=1298&663=1301&665=1303&666=1306&667=1309&668=1311&669=1314&672=1317&673=1320&674=1323&679=1326&682=1329&683=1332&685=1334&686=1337&688=1339&689=1342&690=1345&691=1347&692=1350&695=1353&696=1356&697=1359&702=1362&705=1365&706=1368&707=1371&708=1373&709=1376&711=1378&712=1380&713=1383&715=1388&718=1390&719=1393&724=1396&727=1399&728=1404&729=1407&731=1411&732=1414&734=1418&735=1421&737=1425&738=1428&740=1432&741=1434&742=1436&743=1438&745=1440&746=1442&748=1445&750=1447&751=1449&752=1451&753=1453&755=1456&756=1458&757=1461&759=1463&760=1466&761=1468&762=1471&765=1474&766=1478&767=1481&769=1485&770=1488&772=1492&773=1495&775=1499&776=1502&778=1506&779=1508&780=1510&781=1512&783=1514&784=1516&786=1519&788=1521&789=1524&790=1526&791=1529&794=1532&795=1535&796=1538&798=1545&803=1548&806=1551&807=1554&808=1557&810=1561&811=1564&813=1568&814=1571&815=1573&816=1576&819=1579&820=1582&821=1585&823=1589&824=1592&826=1596&827=1599&828=1601&829=1604&832=1607&833=1611&834=1613&835=1615&836=1617&838=1620&843=1623&846=1626&847=1629&848=1632&849=1634&850=1637&852=1639&853=1642&855=1646&856=1649&859=1654&860=1657&861=1660&862=1662&863=1665&865=1667&866=1670&868=1674&869=1677&874=1682&877=1685&878=1688&879=1691&881=1695&882=1698&884=1702&885=1705&887=1709&888=1712&890=1716&891=1719&892=1721&893=1724&896=1727&897=1730&898=1733&900=1737&901=1740&903=1744&904=1747&906=1751&907=1754&909=1758&910=1761&911=1763&912=1766&915=1769&916=1772&917=1775&919=1782&922=1785&923=1789&924=1791&925=1793&926=1795&927=1797&928=1799&930=1801&931=1803&933=1806&938=1809&941=1812&942=1815&944=1817&945=1820&947=1822&950=1825&951=1828&952=1831&953=1833&954=1836&957=1839&958=1842&959=1845&961=1847&962=1850&964=1854&965=1857&968=1862&969=1866&970=1868&971=1870&973=1873&977=1876&980=1879&981=1882&982=1885&983=1887&984=1890&986=1892&987=1895&989=1899&990=1902&993=1907&994=1910&995=1913&996=1915&997=1918&999=1920&1000=1923&1002=1927&1003=1930&1008=1935&1011=1938&1012=1941&1014=1943&1015=1946&1017=1948&1018=1951&1019=1954&1020=1956&1021=1959&1023=1961&1024=1964&1026=1968&1027=1971&1030=1976&1031=1979&1032=1982&1034=1984&1035=1987&1037=1991&1038=1994&1041=1999&1042=2001&1045=2004&1046=2006&1047=2009&1048=2011&1050=2014&1051=2016&1053=2020&1058=2022&1061=2025&1064=2028&1066=2031&1068=2034&1070=2037&1071=2040&1072=2042&1073=2045&1075=2047&1076=2050&1077=2053&1078=2055&1079=2058&1081=2060&1082=2063&1084=2065&1085=2068&1086=2070&1087=2073&1088=2075&1089=2078&1090=2080&1091=2083&1092=2087&1093=2090&1096=2095&1097=2098&1098=2101&1099=2103&1100=2106&1102=2108&1103=2111&1105=2113&1106=2116&1107=2118&1108=2121&1109=2123&1110=2126&1111=2128&1112=2131&1113=2135&1114=2138&1119=2143&1122=2146&1123=2149&1125=2151&1126=2154&1127=2157&1128=2159&1129=2162&1131=2164&1132=2167&1134=2171&1135=2174&1138=2179&1139=2182&1140=2185&1141=2187&1142=2190&1144=2192&1145=2195&1147=2199&1148=2202&1151=2207&1152=2210&1154=2212&1159=2215&1162=2218&1163=2221&1165=2223&1166=2226&1167=2229&1168=2231&1169=2234&1171=2236&1172=2239&1174=2243&1175=2246&1178=2251&1179=2254&1180=2257&1181=2259&1182=2262&1184=2264&1185=2267&1187=2271&1188=2274&1191=2279&1192=2282&1194=2284&1199=2287&1201=2292&1202=2294&1203=2297&1205=2299&1207=2302&1210=2305&1215=2308&1216=2310&1217=2313&1218=2317&1220=2322&1221=2325&1225=2330&1226=2332&1227=2335&1228=2339&1230=2344&1231=2347&1235=2352&1236=2355&1238=2357&1241=2360&1244=2363&1245=2366&1247=2368&1249=2370&1248=2374&1250=2378&1251=2380&1252=2382&1254=2384&1255=2386&1256=2388&1257=2390&1258=2392&1260=2395&1263=2398&1264=2401&1265=2404&1266=2410&1267=2413&1274=2420&1275=2422&1276=2424&1277=2435&1278=2438&1280=2442&1281=2445&1283=2449&1284=2451&1285=2453&1286=2455&1287=2457&1288=2459&1291=2462&1292=2464&1293=2467&1295=2469&1296=2471&1297=2473&1298=2475&1300=2478&1301=2480&1302=2483&1304=2485&1305=2488&1307=2492&1308=2495&1310=2497&1311=2500&1313=2504&1314=2507&1316=2509&1317=2512&1319=2514&1320=2517&1322=2521&1323=2524&1325=2528&1326=2530&1327=2532&1328=2534&1330=2537&1332=2539&1333=2542&1335=2544&1336=2547&1337=2549&1340=2552&1342=2560&1343=2563&1345=2565&1346=2567&1347=2569&1348=2571&1350=2574&1352=2576&1353=2578&1354=2580&1355=2582&1357=2585&1358=2587&1359=2589&1360=2592&1362=2594&1363=2597&1365=2601&1366=2604&1368=2606&1369=2609&1370=2611&1371=2614&1373=2618&1374=2621&1375=2623&1376=2626&1378=2628&1379=2630&1380=2632&1381=2634&1383=2636&1384=2638&1386=2641&1388=2643&1389=2645&1390=2647&1391=2649&1393=2651&1394=2653&1396=2656&1398=2658&1399=2661&1401=2665&1402=2668&1404=2672&1405=2675&1411=2679&1412=2681&1414=2682&1415=2684&1418=2686&1419=2689&1420=2692&1422=2699&1425=2702&1426=2706&1427=2708&1428=2710&1430=2712&1431=2714&1433=2716&1434=2718&1436=2720&1437=2722&1439=2724&1440=2726&1442=2728&1443=2730&1445=2732&1446=2734&1448=2737&1450=2740&1451=2744&1452=2746&1453=2748&1454=2750&1455=2752&1456=2754&1458=2756&1459=2758&1461=2761&1464=2764&1467=2767&1468=2770&1470=2772&1471=2775&1473=2777&1474=2780&1475=2783&1479=2786&1482=2789&1483=2792&1485=2794&1486=2797&1488=2799&1489=2802&1490=2805&1495=2808&1498=2811&1499=2814&1501=2816&1502=2819&1504=2821&1506=2824&1509=2827&1512=2830&1514=2833&1516=2836&1518=2839&1519=2842&1520=2844&1521=2847&1523=2849&1524=2853&1525=2856&1527=2858&1528=2861&1530=2865&1531=2868&1534=2872&1535=2875&1536=2879&1537=2881&1539=2882&1540=2885&1542=2889&1543=2892&1544=2896&1545=2898&1547=2899&1548=2902&1550=2906&1551=2908&1552=2910&1553=2912&1554=2914&1556=2916&1557=2918&1559=2921&1563=2924&1564=2928&1566=2933&1567=2937&1569=2942&1570=2946&1571=2948&1572=2950&1574=2953&1577=2956&1580=2959&1581=2962&1583=2964&1584=2967&1586=2969&1589=2972&1590=2975&1591=2978&1593=2980&1594=2983&1596=2987&1597=2990&1600=2995&1601=2999&1602=3001&1603=3003&1605=3006&1608=3009&1611=3012&1612=3015&1614=3017&1615=3020&1617=3022&1619=3025&1622=3028&1625=3031&1627=3034&1629=3037&1631=3040&1632=3043&1633=3045&1634=3048&1636=3050&1637=3053&1638=3056&1640=3058&1641=3061&1643=3065&1644=3068&1646=3072&1647=3075&1649=3079&1650=3082&1653=3087&1654=3091&1655=3093&1656=3095&1658=3098&1661=3101&1664=3104&1665=3107&1667=3109&1668=3112&1670=3114&1673=3117&1674=3120&1675=3123&1677=3125&1678=3128&1680=3132&1681=3135&1684=3140&1685=3144&1686=3146&1687=3148&1689=3151&1692=3154&1694=3158&1695=3160&1696=3162&1697=3165&1699=3167&1700=3170&1702=3172&1703=3176&1706=3179&1707=3182&1708=3185&1709=3187&1710=3190&1712=3192&1713=3195&1716=3198&1717=3201&1718=3204&1720=3206&1721=3209&1723=3213&1724=3216&1727=3221&1728=3225&1729=3227&1730=3229&1732=3232&1735=3236&1737=3239&1741=3242&1742=3246&1743=3248&1744=3251'