import { ImportedStyleSheet } from "@bokehjs/core/dom";
import { HTMLBox, HTMLBoxView } from "./layout";
export class ProgressView extends HTMLBoxView {
    static __name__ = "ProgressView";
    progressEl;
    connect_signals() {
        super.connect_signals();
        const render = () => this.render();
        this.connect(this.model.properties.height.change, render);
        this.connect(this.model.properties.width.change, render);
        this.connect(this.model.properties.height_policy.change, render);
        this.connect(this.model.properties.width_policy.change, render);
        this.connect(this.model.properties.sizing_mode.change, render);
        this.connect(this.model.properties.active.change, () => this.setCSS());
        this.connect(this.model.properties.bar_color.change, () => this.setCSS());
        this.connect(this.model.properties.css_classes.change, () => this.setCSS());
        this.connect(this.model.properties.value.change, () => this.setValue());
        this.connect(this.model.properties.max.change, () => this.setMax());
    }
    render() {
        super.render();
        const style = { ...this.model.styles, display: "inline-block" };
        this.progressEl = document.createElement("progress");
        this.setValue();
        this.setMax();
        // Set styling
        this.setCSS();
        for (const prop in style) {
            this.progressEl.style.setProperty(prop, style[prop]);
        }
        this.shadow_el.appendChild(this.progressEl);
    }
    stylesheets() {
        const styles = super.stylesheets();
        for (const css of this.model.css) {
            styles.push(new ImportedStyleSheet(css));
        }
        return styles;
    }
    setCSS() {
        let css = `${this.model.css_classes.join(" ")} ${this.model.bar_color}`;
        if (this.model.active) {
            css = `${css} active`;
        }
        this.progressEl.className = css;
    }
    setValue() {
        if (this.model.value == null) {
            this.progressEl.value = 0;
        }
        else if (this.model.value >= 0) {
            this.progressEl.value = this.model.value;
        }
        else if (this.model.value < 0) {
            this.progressEl.removeAttribute("value");
        }
    }
    setMax() {
        if (this.model.max != null) {
            this.progressEl.max = this.model.max;
        }
    }
}
export class Progress extends HTMLBox {
    static __name__ = "Progress";
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "panel.models.widgets";
    static {
        this.prototype.default_view = ProgressView;
        this.define(({ Any, List, Bool, Float, Str }) => ({
            active: [Bool, true],
            bar_color: [Str, "primary"],
            css: [List(Str), []],
            max: [Float, 100],
            value: [Any, null],
        }));
    }
}
//# sourceMappingURL=progress.js.map