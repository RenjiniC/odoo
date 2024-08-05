/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Component, useState } from "@odoo/owl";
import { Test } from "./owl_session_test"

patch(Test.prototype, {
    reset(){
    console.log('Hello')
    this.state.value : 0

        }
    }
