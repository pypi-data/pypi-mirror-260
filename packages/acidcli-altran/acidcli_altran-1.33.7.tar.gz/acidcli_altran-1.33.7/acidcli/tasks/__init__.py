# Copyright Capgemini Engineering B.V.

"""CICD tasks.

Task implementations for jobs
"""
from acidcli.tasks.acceptance.features.factory import AcceptanceFeatures
from acidcli.tasks.build.binaries.factory import BuildBinaries
from acidcli.tasks.build.documentation.factory import BuildDocumentation
from acidcli.tasks.build.codedocumentation.factory import BuildCodeDocumentation
from acidcli.tasks.check.codeinspection.factory import CheckCodeInspection
from acidcli.tasks.check.codelint.factory import CheckCodeLint
from acidcli.tasks.check.codestyle.factory import CheckCodeStyle
from acidcli.tasks.check.cohesion.factory import CheckCohesion
from acidcli.tasks.check.complexity.factory import CheckComplexity
from acidcli.tasks.check.copyright.factory import CheckCopyright
from acidcli.tasks.check.crimescene.factory import CheckCrimeScene
from acidcli.tasks.check.deadcode.factory import CheckDeadcode
from acidcli.tasks.check.doclint.factory import CheckDocLint
from acidcli.tasks.check.docspell.factory import CheckDocSpell
from acidcli.tasks.check.docstyle.factory import CheckDocStyle
from acidcli.tasks.check.duplication.factory import CheckDuplication
from acidcli.tasks.check.featurelint.factory import CheckFeatureLint
from acidcli.tasks.check.format.factory import CheckFormat
from acidcli.tasks.check.linesofcode.factory import CheckLinesOfCode
from acidcli.tasks.check.vulnerabilities.factory import CheckVulnerabilities
from acidcli.tasks.check.secrets.factory import CheckSecrets
from acidcli.tasks.publish.codequality.factory import PublishCodeQuality
from acidcli.tasks.publish.pages.factory import PublishPages
from acidcli.tasks.release.binaries.factory import ReleaseBinaries
from acidcli.tasks.test.units.factory import TestUnits
from acidcli.tasks.test.integrations.factory import TestIntegrations
