from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-isis.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_isis = resolve('router_isis')
    l_0_isis_auth_cli = resolve('isis_auth_cli')
    l_0_both_key_ids = resolve('both_key_ids')
    l_0_lu_cli = resolve('lu_cli')
    l_0_ti_lfa_cli = resolve('ti_lfa_cli')
    l_0_ti_lfa_srlg_cli = resolve('ti_lfa_srlg_cli')
    try:
        t_1 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_2 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'instance')):
        pass
        yield '!\nrouter isis '
        yield str(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'instance'))
        yield '\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'net')):
            pass
            yield '   net '
            yield str(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'net'))
            yield '\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'is_type')):
            pass
            yield '   is-type '
            yield str(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'is_type'))
            yield '\n'
        for l_1_redistribute_route in t_1(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'redistribute_routes'), 'source_protocol'):
            l_1_redistribute_route_cli = resolve('redistribute_route_cli')
            _loop_vars = {}
            pass
            if t_2(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                pass
                l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'isis'):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' instance', ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'ospf'):
                    pass
                    if t_2(environment.getattr(l_1_redistribute_route, 'include_leaked'), True):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (not t_2(environment.getattr(l_1_redistribute_route, 'ospf_route_type'))):
                        pass
                        continue
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'ospfv3'):
                    pass
                    if (not t_2(environment.getattr(l_1_redistribute_route, 'ospf_route_type'))):
                        pass
                        continue
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['static', 'connected']):
                    pass
                    if t_2(environment.getattr(l_1_redistribute_route, 'include_leaked'), True):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if t_2(environment.getattr(l_1_redistribute_route, 'route_map')):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                yield '   '
                yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                yield '\n'
        l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'router_id')):
            pass
            yield '   router-id ipv4 '
            yield str(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'router_id'))
            yield '\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'log_adjacency_changes'), True):
            pass
            yield '   log-adjacency-changes\n'
        elif t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'log_adjacency_changes'), False):
            pass
            yield '   no log-adjacency-changes\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'mpls_ldp_sync_default'), True):
            pass
            yield '   mpls ldp sync default\n'
        if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'timers'), 'local_convergence'), 'protected_prefixes'), True):
            pass
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'timers'), 'local_convergence'), 'delay')):
                pass
                yield '   timers local-convergence-delay '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'timers'), 'local_convergence'), 'delay'))
                yield ' protected-prefixes\n'
            else:
                pass
                yield '   timers local-convergence-delay protected-prefixes\n'
        if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'enabled')):
            pass
            yield '   set-overload-bit\n'
        if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup')):
            pass
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'delay')):
                pass
                yield '   set-overload-bit on-startup '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'delay'))
                yield '\n'
            elif t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'wait_for_bgp'), 'enabled'), True):
                pass
                if t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'wait_for_bgp'), 'timeout')):
                    pass
                    yield '   set-overload-bit on-startup wait-for-bgp timeout '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'set_overload_bit'), 'on_startup'), 'wait_for_bgp'), 'timeout'))
                    yield '\n'
                else:
                    pass
                    yield '   set-overload-bit on-startup wait-for-bgp\n'
        if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'advertise'), 'passive_only'), True):
            pass
            yield '   advertise passive-only\n'
        if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'interval')):
            pass
            if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'wait_interval')):
                pass
                yield '   spf-interval '
                yield str(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'interval'))
                yield ' '
                yield str(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'wait_interval'))
                yield '\n'
            else:
                pass
                yield '   spf-interval '
                yield str(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'spf_interval'), 'interval'))
                yield '\n'
        if (t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode')) and (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') in ['md5', 'text']) or ((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') == 'sha') and t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'sha'), 'key_id')))) or (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') == 'shared-secret') and t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'shared_secret'), 'profile'))) and t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'shared_secret'), 'algorithm'))))):
            pass
            l_0_isis_auth_cli = str_join(('authentication mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode'), ))
            context.vars['isis_auth_cli'] = l_0_isis_auth_cli
            context.exported_vars.add('isis_auth_cli')
            if (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') == 'sha'):
                pass
                l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' key-id ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'sha'), 'key_id'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
            elif (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'mode') == 'shared-secret'):
                pass
                l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' profile ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'shared_secret'), 'profile'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
                l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' algorithm ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'shared_secret'), 'algorithm'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'rx_disabled'), 'true'):
                pass
                l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' rx-disabled', ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
            yield '   '
            yield str((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli))
            yield '\n'
        else:
            pass
            if (t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode')) and (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') in ['md5', 'text']) or ((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') == 'sha') and t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'sha'), 'key_id')))) or (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') == 'shared-secret') and t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'shared_secret'), 'profile'))) and t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'shared_secret'), 'algorithm'))))):
                pass
                l_0_isis_auth_cli = str_join(('authentication mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
                if (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') == 'sha'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' key-id ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'sha'), 'key_id'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                elif (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'mode') == 'shared-secret'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' profile ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'shared_secret'), 'profile'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' algorithm ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'shared_secret'), 'algorithm'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'rx_disabled'), 'true'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' rx-disabled', ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                yield '   '
                yield str((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli))
                yield ' level-1\n'
            if (t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode')) and (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') in ['md5', 'text']) or ((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') == 'sha') and t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'sha'), 'key_id')))) or (((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') == 'shared-secret') and t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'shared_secret'), 'profile'))) and t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'shared_secret'), 'algorithm'))))):
                pass
                l_0_isis_auth_cli = str_join(('authentication mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode'), ))
                context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                context.exported_vars.add('isis_auth_cli')
                if (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') == 'sha'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' key-id ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'sha'), 'key_id'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                elif (environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'mode') == 'shared-secret'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' profile ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'shared_secret'), 'profile'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' algorithm ', environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'shared_secret'), 'algorithm'), ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'rx_disabled'), 'true'):
                    pass
                    l_0_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli), ' rx-disabled', ))
                    context.vars['isis_auth_cli'] = l_0_isis_auth_cli
                    context.exported_vars.add('isis_auth_cli')
                yield '   '
                yield str((undefined(name='isis_auth_cli') if l_0_isis_auth_cli is missing else l_0_isis_auth_cli))
                yield ' level-2\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart')):
            pass
            if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 'enabled'), True):
                pass
                yield '   graceful-restart\n'
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 't2'), 'level_1_wait_time')):
                pass
                yield '   graceful-restart t2 level-1 '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 't2'), 'level_1_wait_time'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 't2'), 'level_2_wait_time')):
                pass
                yield '   graceful-restart t2 level-2 '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 't2'), 'level_2_wait_time'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 'restart_hold_time')):
                pass
                yield '   graceful-restart restart-hold-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'graceful_restart'), 'restart_hold_time'))
                yield '\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication')):
            pass
            l_0_both_key_ids = []
            context.vars['both_key_ids'] = l_0_both_key_ids
            context.exported_vars.add('both_key_ids')
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key_ids')):
                pass
                for l_1_auth_key in t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key_ids'), 'id'):
                    _loop_vars = {}
                    pass
                    if (((t_2(environment.getattr(l_1_auth_key, 'id')) and t_2(environment.getattr(l_1_auth_key, 'algorithm'))) and t_2(environment.getattr(l_1_auth_key, 'key_type'))) and t_2(environment.getattr(l_1_auth_key, 'key'))):
                        pass
                        context.call(environment.getattr((undefined(name='both_key_ids') if l_0_both_key_ids is missing else l_0_both_key_ids), 'append'), environment.getattr(l_1_auth_key, 'id'), _loop_vars=_loop_vars)
                        if t_2(environment.getattr(l_1_auth_key, 'rfc_5310'), True):
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' rfc-5310 key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield '\n'
                        else:
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield '\n'
                l_1_auth_key = missing
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key_ids')):
                pass
                for l_1_auth_key in environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key_ids'):
                    _loop_vars = {}
                    pass
                    if ((((t_2(environment.getattr(l_1_auth_key, 'id')) and (environment.getattr(l_1_auth_key, 'id') not in (undefined(name='both_key_ids') if l_0_both_key_ids is missing else l_0_both_key_ids))) and t_2(environment.getattr(l_1_auth_key, 'algorithm'))) and t_2(environment.getattr(l_1_auth_key, 'key_type'))) and t_2(environment.getattr(l_1_auth_key, 'key'))):
                        pass
                        if t_2(environment.getattr(l_1_auth_key, 'rfc_5310'), True):
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' rfc-5310 key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield ' level-1\n'
                        else:
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield ' level-1\n'
                l_1_auth_key = missing
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key_ids')):
                pass
                for l_1_auth_key in environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key_ids'):
                    _loop_vars = {}
                    pass
                    if ((((t_2(environment.getattr(l_1_auth_key, 'id')) and (environment.getattr(l_1_auth_key, 'id') not in (undefined(name='both_key_ids') if l_0_both_key_ids is missing else l_0_both_key_ids))) and t_2(environment.getattr(l_1_auth_key, 'algorithm'))) and t_2(environment.getattr(l_1_auth_key, 'key_type'))) and t_2(environment.getattr(l_1_auth_key, 'key'))):
                        pass
                        if t_2(environment.getattr(l_1_auth_key, 'rfc_5310'), True):
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' rfc-5310 key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield ' level-2\n'
                        else:
                            pass
                            yield '   authentication key-id '
                            yield str(environment.getattr(l_1_auth_key, 'id'))
                            yield ' algorithm '
                            yield str(environment.getattr(l_1_auth_key, 'algorithm'))
                            yield ' key '
                            yield str(environment.getattr(l_1_auth_key, 'key_type'))
                            yield ' '
                            yield str(environment.getattr(l_1_auth_key, 'key'))
                            yield ' level-2\n'
                l_1_auth_key = missing
            if (t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key_type')) and t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key'))):
                pass
                yield '   authentication key '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key_type'))
                yield ' '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'both'), 'key'))
                yield '\n'
            else:
                pass
                if (t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key_type')) and t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key'))):
                    pass
                    yield '   authentication key '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key_type'))
                    yield ' '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_1'), 'key'))
                    yield ' level-1\n'
                if (t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key_type')) and t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key'))):
                    pass
                    yield '   authentication key '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key_type'))
                    yield ' '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'authentication'), 'level_2'), 'key'))
                    yield ' level-2\n'
        yield '   !\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family')):
            pass
            for l_1_address_family in environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family'):
                _loop_vars = {}
                pass
                yield '   address-family '
                yield str(l_1_address_family)
                yield '\n'
                if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'isis_af_defaults')):
                    pass
                    for l_2_af_default in environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'isis_af_defaults'):
                        _loop_vars = {}
                        pass
                        yield '      '
                        yield str(l_2_af_default)
                        yield '\n'
                    l_2_af_default = missing
            l_1_address_family = missing
            yield '   !\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4')):
            pass
            yield '   address-family ipv4 unicast\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'maximum_paths')):
                pass
                yield '      maximum-paths '
                yield str(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'maximum_paths'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'tunnel_source_labeled_unicast'), 'enabled'), True):
                pass
                l_0_lu_cli = 'tunnel source-protocol bgp ipv4 labeled-unicast'
                context.vars['lu_cli'] = l_0_lu_cli
                context.exported_vars.add('lu_cli')
                if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'tunnel_source_labeled_unicast'), 'rcf')):
                    pass
                    l_0_lu_cli = str_join(((undefined(name='lu_cli') if l_0_lu_cli is missing else l_0_lu_cli), ' rcf ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'tunnel_source_labeled_unicast'), 'rcf'), ))
                    context.vars['lu_cli'] = l_0_lu_cli
                    context.exported_vars.add('lu_cli')
                yield '      '
                yield str((undefined(name='lu_cli') if l_0_lu_cli is missing else l_0_lu_cli))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'bfd_all_interfaces'), True):
                pass
                yield '      bfd all-interfaces\n'
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'mode')):
                pass
                l_0_ti_lfa_cli = str_join(('fast-reroute ti-lfa mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'mode'), ))
                context.vars['ti_lfa_cli'] = l_0_ti_lfa_cli
                context.exported_vars.add('ti_lfa_cli')
                if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'level')):
                    pass
                    l_0_ti_lfa_cli = str_join(((undefined(name='ti_lfa_cli') if l_0_ti_lfa_cli is missing else l_0_ti_lfa_cli), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'level'), ))
                    context.vars['ti_lfa_cli'] = l_0_ti_lfa_cli
                    context.exported_vars.add('ti_lfa_cli')
                yield '      '
                yield str((undefined(name='ti_lfa_cli') if l_0_ti_lfa_cli is missing else l_0_ti_lfa_cli))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'srlg'), 'enable'), True):
                pass
                l_0_ti_lfa_srlg_cli = 'fast-reroute ti-lfa srlg'
                context.vars['ti_lfa_srlg_cli'] = l_0_ti_lfa_srlg_cli
                context.exported_vars.add('ti_lfa_srlg_cli')
                if t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv4'), 'fast_reroute_ti_lfa'), 'srlg'), 'strict'), True):
                    pass
                    l_0_ti_lfa_srlg_cli = str_join(((undefined(name='ti_lfa_srlg_cli') if l_0_ti_lfa_srlg_cli is missing else l_0_ti_lfa_srlg_cli), ' strict', ))
                    context.vars['ti_lfa_srlg_cli'] = l_0_ti_lfa_srlg_cli
                    context.exported_vars.add('ti_lfa_srlg_cli')
                yield '      '
                yield str((undefined(name='ti_lfa_srlg_cli') if l_0_ti_lfa_srlg_cli is missing else l_0_ti_lfa_srlg_cli))
                yield '\n'
            yield '   !\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6')):
            pass
            yield '   address-family ipv6 unicast\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'maximum_paths')):
                pass
                yield '      maximum-paths '
                yield str(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'maximum_paths'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'bfd_all_interfaces'), True):
                pass
                yield '      bfd all-interfaces\n'
            if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'mode')):
                pass
                l_0_ti_lfa_cli = str_join(('fast-reroute ti-lfa mode ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'mode'), ))
                context.vars['ti_lfa_cli'] = l_0_ti_lfa_cli
                context.exported_vars.add('ti_lfa_cli')
                if t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'level')):
                    pass
                    l_0_ti_lfa_cli = str_join(((undefined(name='ti_lfa_cli') if l_0_ti_lfa_cli is missing else l_0_ti_lfa_cli), ' ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'level'), ))
                    context.vars['ti_lfa_cli'] = l_0_ti_lfa_cli
                    context.exported_vars.add('ti_lfa_cli')
                yield '      '
                yield str((undefined(name='ti_lfa_cli') if l_0_ti_lfa_cli is missing else l_0_ti_lfa_cli))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'srlg'), 'enable'), True):
                pass
                l_0_ti_lfa_srlg_cli = 'fast-reroute ti-lfa srlg'
                context.vars['ti_lfa_srlg_cli'] = l_0_ti_lfa_srlg_cli
                context.exported_vars.add('ti_lfa_srlg_cli')
                if t_2(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'address_family_ipv6'), 'fast_reroute_ti_lfa'), 'srlg'), 'strict'), True):
                    pass
                    l_0_ti_lfa_srlg_cli = str_join(((undefined(name='ti_lfa_srlg_cli') if l_0_ti_lfa_srlg_cli is missing else l_0_ti_lfa_srlg_cli), ' strict', ))
                    context.vars['ti_lfa_srlg_cli'] = l_0_ti_lfa_srlg_cli
                    context.exported_vars.add('ti_lfa_srlg_cli')
                yield '      '
                yield str((undefined(name='ti_lfa_srlg_cli') if l_0_ti_lfa_srlg_cli is missing else l_0_ti_lfa_srlg_cli))
                yield '\n'
            yield '   !\n'
        if t_2(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'segment_routing_mpls')):
            pass
            yield '   segment-routing mpls\n'
            if t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'segment_routing_mpls'), 'enabled'), True):
                pass
                yield '      no shutdown\n'
            elif t_2(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'segment_routing_mpls'), 'enabled'), False):
                pass
                yield '      shutdown\n'
            for l_1_prefix_segment in t_1(environment.getattr(environment.getattr((undefined(name='router_isis') if l_0_router_isis is missing else l_0_router_isis), 'segment_routing_mpls'), 'prefix_segments'), 'prefix'):
                _loop_vars = {}
                pass
                if (t_2(environment.getattr(l_1_prefix_segment, 'prefix')) and t_2(environment.getattr(l_1_prefix_segment, 'index'))):
                    pass
                    yield '      prefix-segment '
                    yield str(environment.getattr(l_1_prefix_segment, 'prefix'))
                    yield ' index '
                    yield str(environment.getattr(l_1_prefix_segment, 'index'))
                    yield '\n'
            l_1_prefix_segment = missing

blocks = {}
debug_info = '7=29&9=32&10=34&11=37&13=39&14=42&16=44&17=48&18=50&19=52&20=54&21=56&22=58&23=60&25=62&26=64&28=65&29=67&30=69&31=71&33=72&34=74&35=76&36=78&39=80&40=82&42=85&45=88&46=91&48=93&50=96&53=99&56=102&57=104&58=107&63=112&66=115&67=117&68=120&69=122&70=124&71=127&77=132&80=135&81=137&82=140&84=147&87=149&93=151&94=154&95=156&96=159&97=161&98=164&100=167&101=169&103=173&105=177&111=179&112=182&113=184&114=187&115=189&116=192&118=195&119=197&121=201&123=203&129=205&130=208&131=210&132=213&133=215&134=218&136=221&137=223&139=227&142=229&143=231&146=234&147=237&149=239&150=242&152=244&153=247&156=249&157=251&158=254&159=256&160=259&164=261&165=262&166=265&168=276&173=285&174=287&175=290&180=292&181=295&183=306&188=315&189=317&190=320&195=322&196=325&198=336&203=345&204=348&206=354&207=357&209=361&210=364&215=369&216=371&217=375&218=377&219=379&220=383&226=388&228=391&229=394&231=396&232=398&233=401&234=403&236=407&238=409&241=412&242=414&243=417&244=419&246=423&248=425&249=427&250=430&251=432&253=436&257=439&259=442&260=445&262=447&265=450&266=452&267=455&268=457&270=461&272=463&273=465&274=468&275=470&277=474&281=477&283=480&285=483&288=486&289=489&290=492'