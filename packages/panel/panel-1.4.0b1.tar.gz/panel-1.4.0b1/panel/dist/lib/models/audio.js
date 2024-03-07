import { HTMLBox, HTMLBoxView, set_size } from "./layout";
export class AudioView extends HTMLBoxView {
    static __name__ = "AudioView";
    audioEl;
    dialogEl;
    _blocked;
    _time;
    _setting;
    initialize() {
        super.initialize();
        this._blocked = false;
        this._setting = false;
        this._time = Date.now();
    }
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.loop.change, () => this.set_loop());
        this.connect(this.model.properties.paused.change, () => this.set_paused());
        this.connect(this.model.properties.time.change, () => this.set_time());
        this.connect(this.model.properties.value.change, () => this.set_value());
        this.connect(this.model.properties.volume.change, () => this.set_volume());
        this.connect(this.model.properties.muted.change, () => this.set_muted());
        this.connect(this.model.properties.autoplay.change, () => this.set_autoplay());
    }
    render() {
        super.render();
        this.audioEl = document.createElement("audio");
        this.audioEl.controls = true;
        this.audioEl.src = this.model.value;
        this.audioEl.currentTime = this.model.time;
        this.audioEl.loop = this.model.loop;
        this.audioEl.muted = this.model.muted;
        this.audioEl.autoplay = this.model.autoplay;
        if (this.model.volume != null) {
            this.audioEl.volume = this.model.volume / 100;
        }
        else {
            this.model.volume = this.audioEl.volume * 100;
        }
        this.audioEl.onpause = () => this.model.paused = true;
        this.audioEl.onplay = () => this.model.paused = false;
        this.audioEl.ontimeupdate = () => this.update_time(this);
        this.audioEl.onvolumechange = () => this.update_volume(this);
        set_size(this.audioEl, this.model, false);
        this.shadow_el.appendChild(this.audioEl);
        if (!this.model.paused) {
            this.audioEl.play();
        }
    }
    update_time(view) {
        if (view._setting) {
            view._setting = false;
            return;
        }
        if ((Date.now() - view._time) < view.model.throttle) {
            return;
        }
        view._blocked = true;
        view.model.time = view.audioEl.currentTime;
        view._time = Date.now();
    }
    update_volume(view) {
        if (view._setting) {
            view._setting = false;
            return;
        }
        view._blocked = true;
        view.model.volume = view.audioEl.volume * 100;
    }
    set_loop() {
        this.audioEl.loop = this.model.loop;
    }
    set_muted() {
        this.audioEl.muted = this.model.muted;
    }
    set_autoplay() {
        this.audioEl.autoplay = this.model.autoplay;
    }
    set_paused() {
        if (!this.audioEl.paused && this.model.paused) {
            this.audioEl.pause();
        }
        if (this.audioEl.paused && !this.model.paused) {
            this.audioEl.play();
        }
    }
    set_volume() {
        if (this._blocked) {
            this._blocked = false;
            return;
        }
        this._setting = true;
        if (this.model.volume != null) {
            this.audioEl.volume = this.model.volume / 100;
        }
    }
    set_time() {
        if (this._blocked) {
            this._blocked = false;
            return;
        }
        this._setting = true;
        this.audioEl.currentTime = this.model.time;
    }
    set_value() {
        this.audioEl.src = this.model.value;
    }
}
export class Audio extends HTMLBox {
    static __name__ = "Audio";
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "panel.models.widgets";
    static {
        this.prototype.default_view = AudioView;
        this.define(({ Any, Bool, Float, Nullable }) => ({
            loop: [Bool, false],
            paused: [Bool, true],
            muted: [Bool, false],
            autoplay: [Bool, false],
            time: [Float, 0],
            throttle: [Float, 250],
            value: [Any, ""],
            volume: [Nullable(Float), null],
        }));
    }
}
//# sourceMappingURL=audio.js.map