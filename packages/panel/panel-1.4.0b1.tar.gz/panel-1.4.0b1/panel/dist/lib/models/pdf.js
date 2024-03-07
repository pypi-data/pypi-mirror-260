import { Markup } from "@bokehjs/models/widgets/markup";
import { PanelMarkupView } from "./layout";
import { htmlDecode } from "./html";
export class PDFView extends PanelMarkupView {
    static __name__ = "PDFView";
    connect_signals() {
        super.connect_signals();
        const p = this.model.properties;
        const { text, width, height, embed, start_page } = p;
        this.on_change([text, width, height, embed, start_page], () => {
            this.update();
        });
    }
    render() {
        super.render();
        this.update();
    }
    update() {
        if (this.model.embed) {
            const blob = this.convert_base64_to_blob();
            const url = URL.createObjectURL(blob);
            const w = this.model.width || "100%";
            const h = this.model.height || "100%";
            this.container.innerHTML = `<embed src="${url}#page=${this.model.start_page}" type="application/pdf" width="${w}" height="${h}"></embed>`;
        }
        else {
            const html = htmlDecode(this.model.text);
            this.container.innerHTML = html || "";
        }
    }
    convert_base64_to_blob() {
        const byteCharacters = atob(this.model.text);
        const sliceSize = 512;
        const byteArrays = [];
        for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            const slice = byteCharacters.slice(offset, offset + sliceSize);
            const byteNumbers = new Uint8Array(slice.length);
            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }
            byteArrays.push(byteNumbers);
        }
        return new Blob(byteArrays, { type: "application/pdf" });
    }
}
export class PDF extends Markup {
    static __name__ = "PDF";
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "panel.models.markup";
    static {
        this.prototype.default_view = PDFView;
        this.define(({ Float, Bool }) => ({
            embed: [Bool, true],
            start_page: [Float, 1],
        }));
    }
}
//# sourceMappingURL=pdf.js.map