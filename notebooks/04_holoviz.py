#!/usr/bin/env python

import numpy as np
import panel as pn
import param
import holoviews as hv
from holoviews import streams
from holoviews import opts
from holoviews.operation.datashader import rasterize

pn.extension('vtk')
hv.extension("bokeh")

class Sinewave(param.Parameterized):
    amp = param.Number(default=1.0, bounds=(0, None), doc="almplitude")
    phase = param.Number(default=0.0, bounds=(0, np.pi*2), doc="phase")

    @param.depends("amp", "phase")
    def viewer(self):
        x = np.linspace(0, 4*np.pi, 100)
        y = self.amp* np.sin(x + self.phase)
        
        scatter1 = hv.Scatter((x, y), label='Asin(x+b)')
        scatter2 = hv.Scatter((x, y*2), label='2A*sin(x+b)').opts(color='orange')
        scatter3 = hv.Scatter((x, y*3), label='3A*sin(x+b)').opts(color='green')
        scatter4 = hv.Scatter(scatter3).opts(line_color='green', marker='square', fill_alpha=0, size=5)

        curve1 = hv.Curve(scatter1)
        curve2 = hv.Curve(scatter2).opts(line_dash=(4, 4), color='orange')
        curve3 = hv.Curve(scatter3).opts(color='orange')
        
        example1 = scatter1 * scatter2 * scatter3
        example2 = scatter1 *  curve1 * curve2 * scatter4 * curve3
        return example1.relabel("Example") + example2.relabel("Another Example")

    def panel(self):
        amp_input = pn.widgets.FloatInput.from_param(self.param.amp)
        phase_input = pn.widgets.FloatSlider.from_param(self.param.phase)
        return pn.Column(
            amp_input,
            phase_input,
            self.viewer,
        )

app = Sinewave().panel()
pn.template.FastListTemplate(
    site="iMars3D demo",
    title="Neutron Image Reconstruction",
    logo="HFIR_SNS_logo.png",
    header_background="#00A170",
    main=app,
    # theme="dark",
    theme_toggle=True,
).servable()
