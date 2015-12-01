#!/bin/bash

{{ mailhog.pkg_dest }} -ui-bind-addr 0.0.0.0:{{ mailhog.web_port }} -api-bind-addr 0.0.0.0:{{ mailhog.web_port }} -smtp-bind-addr 0.0.0.0:{{ mailhog.smtp_port }}
