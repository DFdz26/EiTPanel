import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Status");
    }

    async getHtml() {
        return `
            <section class="center"> 
                <section class="title">
                    <h2> Mission status </h2>
                </section>
                <p>
                    Maybe we will do, maybe not xD
                </p>
                <p>
                    <a href="/" data-link>New mission</a>.
                </p>
            </section>
        `;
    }
}