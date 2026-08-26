#!/usr/bin/env python3
import aws_cdk as cdk  # type: ignore[reportMissingImports]

from contador_stack import ContadorAcessosStack

app = cdk.App()
ContadorAcessosStack(app, "ContadorAcessosStack")
app.synth()
