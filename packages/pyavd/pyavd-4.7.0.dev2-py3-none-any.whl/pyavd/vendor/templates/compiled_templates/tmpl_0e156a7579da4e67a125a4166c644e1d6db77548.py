from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/monitor-layer1.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_monitor_layer1 = resolve('monitor_layer1')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_2(environment.getattr((undefined(name='monitor_layer1') if l_0_monitor_layer1 is missing else l_0_monitor_layer1), 'enabled'), True):
        pass
        yield '\n## Monitor Layer 1 Logging\n\n| Layer 1 Event | Logging |\n| ------------- | ------- |\n| MAC fault | '
        yield str(t_1(environment.getattr((undefined(name='monitor_layer1') if l_0_monitor_layer1 is missing else l_0_monitor_layer1), 'logging_mac_fault'), False))
        yield ' |\n| Transceiver DOM | '
        yield str(t_1(environment.getattr(environment.getattr((undefined(name='monitor_layer1') if l_0_monitor_layer1 is missing else l_0_monitor_layer1), 'logging_transceiver'), 'dom'), False))
        yield ' |\n| Transceiver communication | '
        yield str(t_1(environment.getattr(environment.getattr((undefined(name='monitor_layer1') if l_0_monitor_layer1 is missing else l_0_monitor_layer1), 'logging_transceiver'), 'communication'), False))
        yield ' |\n\n### Monitor Layer 1 Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/monitor-layer1.j2', 'documentation/monitor-layer1.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '7=24&13=27&14=29&15=31&20=33'