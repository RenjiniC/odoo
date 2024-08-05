/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Test } from "./owl_session_test"

export class Counter extends Component {
    static template = "test_owl.Counter";
    static components = { Test };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }
    decrement() {
        this.state.value--;
    }

}
registry.category('actions').add('test_owl.Counter', Counter)