# Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import attr
from contextlib import contextmanager
import os
from pathlib import Path
import subprocess

import grpc

from hgitaly.testing.grpc import wait_server_accepts_connection

HGITALY_SOURCE_ROOT = Path(__file__).parent.parent


@attr.s
class RHGitalyServer:
    home_dir = attr.ib()

    @contextmanager
    def running(self):
        env = dict(os.environ)
        env['GITALY_TESTING_NO_GIT_HOOKS'] = "1"  # will be eventually useful
        timeout = int(env.pop('RHGITALY_STARTUP_TIMEOUT', '30').strip())

        env['RHGITALY_REPOSITORIES_ROOT'] = str(self.home_dir / 'default')
        socket_path = self.home_dir / 'rhgitaly.socket'
        url = 'unix:%s' % socket_path.resolve()
        env['RHGITALY_LISTEN_URL'] = url
        rhgitaly_dir = HGITALY_SOURCE_ROOT / 'rust/rhgitaly'

        rhgitaly_exe = env.get('RHGITALY_EXECUTABLE')
        if rhgitaly_exe is None:  # pragma no cover
            subprocess.check_call(('cargo', 'build', '--locked'),
                                  cwd=rhgitaly_dir)
            run_cmd = ('cargo', 'run')
        else:  # pragma no cover
            # Popen would not run a relative binary so easily
            run_cmd = [Path(rhgitaly_exe).resolve()]

        with open(self.home_dir / 'rhgitaly.log', 'w') as logf:
            rhgitaly = subprocess.Popen(
                run_cmd,
                stdout=logf, stderr=logf,
                env=env,
                cwd=rhgitaly_dir,
            )

        try:
            # tonic (actually H2) does not accept the default authority
            # set in the case of Unix Domain Sockets by gRPC 1.58.
            # See https://github.com/hyperium/tonic/issues/742 and for instance
            # this solution by k8s clients:
            # https://github.com/kubernetes/kubernetes/pull/112597
            with grpc.insecure_channel(
                    url,
                    options=[('grpc.default_authority', 'localhost')]
            ) as channel:
                wait_server_accepts_connection(channel, timeout=timeout)
                yield channel
        finally:
            rhgitaly.terminate()
            rhgitaly.wait()
