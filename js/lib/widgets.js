var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');

var pj = require('pretty-json-warfares');

// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var HelloModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'HelloModel',
        _view_name : 'HelloView',
        _model_module : 'crawlab',
        _view_module : 'crawlab',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        value : 'Hello World'
    })
});


// Custom View. Renders the widget model.
var HelloView = widgets.DOMWidgetView.extend({
    render: function() {
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
    },

    value_changed: function() {
        this.el.textContent = this.model.get('value');
    }
});

var BrowserView = widgets.DOMWidgetView.extend({
    template: _.template(
        '<iframe srcdoc="<%= srcdoc %>" width="100%", height="280px"></iframe>'
    ),
    
    render: function() {
        this.$el.html(this.template({'srcdoc': this.model.get('srcdoc')}));
    },
    
});


var JsonView = widgets.DOMWidgetView.extend({
    render: function() {
        var node = new pj.default.view.Node({
          el: this.$el,
          data: this.model.get('data')
        });
    },
    
});



module.exports = {
    HelloModel : HelloModel,
    HelloView : HelloView,
    BrowserView: BrowserView,
    JsonView: JsonView
};
