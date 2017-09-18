# Visit 2.13.0 log file
ScriptVersion = "2.13.0"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
ShowAllWindows()
OpenDatabase("/global/cscratch1/sd/groberts/VisitKNLRebuild/Testing/eek.eek", 0)
# The UpdateDBPluginInfo RPC is not supported in the VisIt module so it will not be logged.
CloseComputeEngine("nid09068", "")
launchArguments = ("-thread", "1", "-withhold-timing-output", "-debug", "5")
OpenComputeEngine("localhost", launchArguments)
# MAINTENANCE ISSUE: SetDefaultFileOpenOptionsRPC is not handled in Logging.C. Please contact a VisIt developer.
OpenDatabase("/global/cscratch1/sd/groberts/VisitKNLRebuild/Testing/eek.eek", 1)
AddPlot("Contour", "temperature", 1, 1)
DrawPlots()
SetActivePlots(0)
DeleteActivePlots()
CloseComputeEngine("nid09068", "")
launchArguments = ("-thread", "16", "-withhold-timing-output", "-debug", "5")
OpenComputeEngine("localhost", launchArguments)
# MAINTENANCE ISSUE: SetDefaultFileOpenOptionsRPC is not handled in Logging.C. Please contact a VisIt developer.
OpenDatabase("/global/cscratch1/sd/groberts/VisitKNLRebuild/Testing/eek.eek", 1)
AddPlot("Contour", "temperature", 1, 1)
DrawPlots()
SetActivePlots(0)
DeleteActivePlots()
CloseComputeEngine("nid09068", "")
launchArguments = ("-thread", "30", "-withhold-timing-output", "-debug", "5")
OpenComputeEngine("localhost", launchArguments)
# MAINTENANCE ISSUE: SetDefaultFileOpenOptionsRPC is not handled in Logging.C. Please contact a VisIt developer.
OpenDatabase("/global/cscratch1/sd/groberts/VisitKNLRebuild/Testing/eek.eek", 1)
AddPlot("Contour", "temperature", 1, 1)
DrawPlots()
SetActivePlots(0)
DeleteActivePlots()
CloseComputeEngine("nid09068", "")
launchArguments = ("-thread", "32", "-withhold-timing-output", "-debug", "5")
OpenComputeEngine("localhost", launchArguments)
# MAINTENANCE ISSUE: SetDefaultFileOpenOptionsRPC is not handled in Logging.C. Please contact a VisIt developer.
OpenDatabase("/global/cscratch1/sd/groberts/VisitKNLRebuild/Testing/eek.eek", 1)
AddPlot("Contour", "temperature", 1, 1)
DrawPlots()
