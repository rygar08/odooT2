/** @odoo-module **/

import { Component, useState , xml } from "@odoo/owl";
import { Counter } from "./components/counter";
import { Card } from "./components/card";

export class Playground extends Component {
    static template = xml`
        <Counter></Counter>
        <Counter></Counter>
        <Card title="'card 1'" content="'content of card 1'"/>
        <Card title="'card 2'" content="'content of card 2'"/>
    ;`


     static components = { Counter, Card };
     setup() {
       // onError((e) => {
       //   console.error(e);
       //   alert('An error occurred. Check the console for more information.');
       // });

      }
}
