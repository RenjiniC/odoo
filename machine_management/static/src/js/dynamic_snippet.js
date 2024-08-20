/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";
export function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
var NewMachines = publicWidget.Widget.extend({
   selector: '.dynamic_snippet',
   willStart: async function () {
       const data = await jsonrpc('/machines', {}).then((data) => {
        console.log('abc',data)
       const [machines] = data
       console.log('helloooo',machines)
       Object.assign(this,{machines})
    })
   },
   start : function () {
        const refEl = this.$el.find("#new_machines_carousel")
        const {machines} = this
        const chunkData = chunk(machines, 4)
        console.log('Happyy.....', chunkData)
        refEl.html(renderToElement('machine_management.new_machine', {
        machines, chunkData
        }))
   }
   });
publicWidget.registry.DynamicSnippet = NewMachines;
return NewMachines;
















///** @odoo-module **/
//import publicWidget from "@web/legacy/js/public/public_widget";
//import { jsonrpc } from "@web/core/network/rpc_service";
//publicWidget.registry.DynamicSnippet = publicWidget.Widget.extend({
//   selector: '.dynamic_snippet',
//   start: function () {
//       var self = this;
//       var data = jsonrpc('/machines', {}).then((data) => {
//           self.$target.empty().append(data)
//       });
//   }
//});
