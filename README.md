# k8-logging-sidecar
The k8 logging sidecar monitors the standard output of an app in the same pod and writes it to disk

# To do
Create json config file containing the logging endpoint(s) intended to log to.
Add it to a list of loggers within the app and push to all of the enabled endpoints.
