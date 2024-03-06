param ($nunit3_input, $junit_output)

$xml = $nunit3_input
$output = $junit_output
Write-Output $output
$junit_xslt = Join-Path ($PSScriptRoot) nunit3_to_junit.xslt
$xslt = New-Object System.Xml.Xsl.XslCompiledTransform;
$xslt.Load($junit_xslt);
$xslt.Transform($xml, $output);
