<script context="module" lang="ts">
	export { default as BaseCheckbox } from "./shared/Checkbox.svelte";
</script>

<script lang="ts">
    import { writable } from 'svelte/store';
    import type { Gradio } from "@gradio/utils";
    import { Block, Info } from "@gradio/atoms";
    import { StatusTracker } from "@gradio/statustracker";
    import type { LoadingStatus } from "@gradio/statustracker";
    import type { SelectData } from "@gradio/utils";
    import { afterUpdate } from "svelte";

    export let elem_id = "";
    export let elem_classes: string[] = [];
    export let visible: boolean = true;
    export let value: boolean = false;
    export let value_is_output = false;
    export let label = "Toggle";
    export let show_label = true;
    export let info: string | undefined = undefined;
    export let container: boolean = true;
    export let scale: number | null = null;
    export let min_width: number | undefined = undefined;
    export let loading_status: LoadingStatus;
    export let gradio: Gradio<{
        change: never;
        select: SelectData;
        input: never;
    }>;
    
    export let interactive: boolean = true;
    
    
    function handle_keydown(event: KeyboardEvent): void {
        if (event.key === 'Enter' || event.key === ' ') {
            handle_change();
        }
    }

    function handle_change(): void {
        if (interactive) {
            value = !value;
            gradio.dispatch("change");
            if (!value_is_output) {
                gradio.dispatch("input");
            }
        }
    }
    afterUpdate(() => {
        value_is_output = false;
    });
</script>

<style>
    .toggle-switch {
        position: relative;
        margin: -8px 0px;
        width: 50px;
        height: 24px;
        display: inline-block;
        border-radius: 12px;
        background: var(--button-secondary-background-fill);
        border: var(--button-border-width) solid var(--button-secondary-border-color);
        cursor: pointer;
        transition: var(--button-transition);
    }

    .toggle-switch::after {
        content: '';
        position: absolute;
        top: 2px;
        left: 1px;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background-color: white;
        border: var(--button-border-width) solid var(--button-secondary-border-color);
        box-shadow: var(--button-shadow-hover);
        transition: transform 0.2s;
    }

    .toggle-switch.active {
        background: var(--checkbox-background-color-selected);
    }

    .toggle-switch.active::after {
        transform: translateX(26px);
    }

    .toggle-switch.non-interactive {
        cursor: not-allowed;
        opacity: 0.6;
    }
    
    .toggle-label {
        font-size: var(--checkbox-label-text-size);
        margin-right: var(--spacing-md);
        color: var(--body-text-color);
        cursor: pointer;
        font-weight: var(--checkbox-label-text-weight);
        line-height: var(--line-md);
        font-family: var(--font);
    }
    
    .toggle-info {
        margin-top: var(--spacing-lg);
    }
</style>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
    <StatusTracker
        autoscroll={gradio.autoscroll}
        i18n={gradio.i18n}
        {...loading_status}
    />
    
    <div class="toggle-container">
        {#if show_label}
            <span
                class="toggle-label"
                aria-hidden="true"
            >
                {label}
            </span>
        {/if}
        
        <div
            class="toggle-switch"
            class:active={value}
            class:non-interactive={!interactive}
            on:click={handle_change}
            on:keydown={handle_keydown}
            tabindex="0"
            type="button"
            role="switch"
            aria-checked={value}
            aria-label={label}
        >
        </div>
        
        {#if info}
            <div class="toggle-info"><Info>{info}</Info></div>
        {/if}
    </div>
    
</Block>
