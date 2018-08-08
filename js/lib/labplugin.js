var crawlab = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'crawlab',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'crawlab',
          version: crawlab.version,
          exports: crawlab
      });
  },
  autoStart: true
};

