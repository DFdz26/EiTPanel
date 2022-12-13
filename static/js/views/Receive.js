import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Receive");
    }

    async getHtml() {
        return `
            <section class="center"> 
            <section class="title">
                <h2> Mission Control </h2>
            </section>

            <p>
                After pickup choose next goal
            </p>
            
            <section class="selections"> 
                <a href="/continue_mission" class="btn Introduce">Next Station</a>
                <a href="/go_home" class="btn Introduce">Go Charging</a>
                <a href="/cancel" class="btn Introduce">Cancel Mission</a>
            </section>
        `;
    }
}