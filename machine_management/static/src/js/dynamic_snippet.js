/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
console.log("dfghjksdfguif")
publicWidget.registry.DynamicSnippet = publicWidget.Widget.extend({
   selector: '.dynamic_snippet',
   start: function () {
       var self = this;
       var data = jsonrpc('/machine', {}).then((data) => {
           self.$target.empty().append(data)
       console.log('hellooooooo')
       });
   }
});

export default publicWidget.registry.DynamicSnippet;



///** @odoo-module */
//import PublicWidget from "@web/legacy/js/public/public_widget";
//import { jsonrpc } from "@web/core/network/rpc_service";
//import { renderToElement } from "@web/core/utils/render";
//console.log("dfghjksdfguif")
//export function _chunk(array, size) {
//    const result = [];
//    for (let i = 0; i < array.length; i += size) {
//        result.push(array.slice(i, i + size));
//    }
//    return result;
//}
//var NewMachines = PublicWidget.Widget.extend({
//        selector: '.dynamic_snippet',
//        willStart: async function () {
//            const data = await jsonrpc('/machines', {})
//            const [machines, website_id] = data
//            Object.assign(this, {
//                machines, website_id
//            })
//        },
//        start: function () {
//            const refEl = this.$el.find("#machine_carousel")
//            const { products, categories, current_website_id, products_list} = this
//            const chunkData = chunk(machines, 4)
//            refEl.html(renderToElement('machine_management.new_machine', {
//                machines,
//                current_website_id,
//                products_list,
//                chunkData
//            }))
//        }
//    });
//PublicWidget.registry.new_machine_snippet = NewMachines;
//return NewMachines;
