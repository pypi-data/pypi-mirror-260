# Copyright (C) 2024 Collimator, Inc.
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, version 3. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General
# Public License for more details.  You should have received a copy of the GNU
# Affero General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

import jax.numpy as jnp

from collimator.framework import LeafSystem


class CartPole(LeafSystem):
    def __init__(
        self, *args, x0=jnp.zeros(4), m_c=5.0, m_p=1.0, L=2.0, g=9.81, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.declare_parameter("m_c", m_c)
        self.declare_parameter("m_p", m_p)
        self.declare_parameter("L", L)
        self.declare_parameter("g", g)

        self.declare_input_port(name="fx")

        self.declare_continuous_state(shape=(4,), ode=self.ode, default_value=x0)
        self.declare_output_port(self._eval_output, default_value=x0[0])

    def _eval_output(
        self, time, state, *inputs, **params
    ):  # output port evaluation of cart position (x)
        x = state.continuous_state[0]
        return x

    def ode(self, time, state, *inputs, **parameters):
        x, theta, dot_x, dot_theta = state.continuous_state
        (fx,) = inputs

        m_c = parameters["m_c"]
        m_p = parameters["m_p"]
        L = parameters["L"]
        g = parameters["g"]

        mf = 1.0 / (m_c + m_p * jnp.sin(theta) ** 2)
        ddot_x = mf * (
            fx + m_p * jnp.sin(theta) * (L * dot_theta**2 + g * jnp.cos(theta))
        )
        ddot_theta = (
            (1.0 / L)
            * mf
            * (
                -fx * jnp.cos(theta)
                - m_p * L * dot_theta**2 * jnp.cos(theta) * jnp.sin(theta)
                - (m_c + m_p) * g * jnp.sin(theta)
            )
        )

        return jnp.array([dot_x, dot_theta, ddot_x[0], ddot_theta[0]])


def animate_cartpole(time, x, theta, x_eq, L=1):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, FFMpegWriter
    from IPython.display import HTML

    fig, ax = plt.subplots()
    ax.set_xlim([jnp.min(x) - L, jnp.max(x) + L])
    ax.set_ylim([-1.5 * L, 1.5 * L])
    ax.set_aspect("equal", "box")

    (line,) = ax.plot([], [], "-bo", markersize=6, lw=2)
    (cart,) = ax.plot([], [], "ks", markersize=18)

    ax.plot([x_eq[0]], [0], "rx")

    def init():
        line.set_data([], [])
        cart.set_data([], [])
        return line, cart

    def update(frame):
        cart_x = x[frame]
        pole_x = cart_x + L * jnp.sin(theta[frame])
        pole_y = -L * jnp.cos(theta[frame])

        line.set_data([cart_x, pole_x], [0, pole_y])
        cart.set_data([cart_x], [0])
        return line, cart

    ani = FuncAnimation(
        fig, update, frames=len(time), init_func=init, blit=True, interval=10
    )

    # Check if the code is running in a Jupyter notebook
    try:
        cfg = get_ipython().config  # noqa: F841
        in_notebook = True
    except NameError:
        in_notebook = False

    if in_notebook:
        plt.close(fig)
        html_content = HTML(ani.to_html5_video())
        return html_content

    try:
        writer = FFMpegWriter(fps=60, metadata={"artist": "Me"}, bitrate=1800)
        savefilename = "cartpole.mp4"
        ani.save(savefilename, writer=writer)
        print(f"Animation saved as {savefilename}")
    except RuntimeError as e:
        print(f"Error saving animation: {e}")
        plt.close()
