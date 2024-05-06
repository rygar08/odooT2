/** @odoo-module */

import { Component, useState, xml } from "@odoo/owl";

export class Counter extends Component {
    static template = xml`
        <div class="m-2 p-2 border d-inline-block">
            <span class="me-2">Counter: <t t-esc="state.value"/></span>
            <button class="btn btn-primary" t-on-click="increment">Increment</button>
        </div>
    `;
//    static components = { SubComponent };
//    static props = { initialValue: Number};
//    static defaultProps = { initialValue: 0};

    setup() {
        this.state = useState({ value: 1 });
//        onWillUpdateProps(nextProps => {
//          return this.loadData({id: nextProps.id});
//        });
//        onMounted(() => {
//          // add some listener
//        });
//        onWillUnmount(() => {
//          // remove listener
//        });
//        onWillPatch(() => {
//          this.scrollState = this.getScrollSTate();
//        });
//        onWillDestroy(() => {
//          // do some cleanup
//        });
//        onError(() => {
//          // do something
//        });
    }

    increment() {
        this.state.value = this.state.value + 1;
    }
}