import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Send");
    }

    async getHtml() {
        return `
            <section class="center"> 
            <section class="title">
                <h2> MiR control </h2>
            </section>
            
            <section class="selections"> 
                <a href="#" class="btn Scan">Scan Barcode</a>
        
                <a href="#" class="btn Introduce">Introduce Barcode</a>
        
                <a href="#" class="btn Move">Move the robot</a>
            </section>
        `;
    }
}