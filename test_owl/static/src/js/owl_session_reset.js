/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Component, useState } from "@odoo/owl";
import { Counter } from "./owl_session"

patch(Counter.prototype, {
    setup(){
        super.setup(...arguments);
    },
    reset(){
    this.state.value = 0
        }
    })
