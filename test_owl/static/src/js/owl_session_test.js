/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Test extends Component {
    static template = "test_owl.Test";
    static defaultProps = {
        a: '',
    };
    setup() {
       console.log('hi')
    };
}
