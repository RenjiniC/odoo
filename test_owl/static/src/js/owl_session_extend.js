/** @odoo-module **/

import { Counter } from "./owl_session"
import { registry } from "@web/core/registry";

class ExtendCounter extends Counter {
static template = 'owl_session_extend.xml';
extend() {
    this.state.value=0;
}
}
registry.category('actions').add('test_owl.extend_counter', ExtendCounter)