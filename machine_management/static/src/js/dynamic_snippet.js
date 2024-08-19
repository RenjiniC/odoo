/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
publicWidget.registry.DynamicSnippet = publicWidget.Widget.extend({
   selector: '.dynamic_snippet',
   start: function () {
       var self = this;
       var data = jsonrpc('/machines', {}).then((data) => {
           self.$target.empty().append(data)
       });
   }
});
