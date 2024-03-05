<svelte:options accessors={true} />

<script context="module" lang="ts">
	export { default as BaseImageUploader } from "./shared/UploadHandler.svelte";
	export { default as BaseStaticImage } from "./shared/UploadHandler.svelte";
	export { default as BaseExample } from "./Example.svelte";
    
</script>

<script lang="ts">
    import { Play as subIcon } from "@gradio/icons";
    import type { Gradio } from "@gradio/utils";
	import ImagePreview from "./shared/ImagePreview.svelte";
    import RemoveFile from "./shared/RemoveFile.svelte";
    import { Upload, ModifyUpload } from "@gradio/upload";
	import UploadHandler from "./shared/UploadHandler.svelte";

    import { Block, BlockTitle, IconButton} from '@gradio/atoms';
	import { StatusTracker} from "@gradio/statustracker";
    import { tick } from "svelte";
    import UploadButton from "./shared/UploadButton.svelte";
    import { createEventDispatcher, onMount } from 'svelte';

    /* Type Imports*/
    import type { LoadingStatus } from "@gradio/statustracker";

    import { FileData } from '@gradio/client';
    
    /* Exports */

    //export let label: string;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;

    export let textValue = "";
    export let images: FileData[] = [];
    export let tempFile: null | FileData[] = null;
    export let value = {"text":textValue, "images": images};
	//export let placeholder = "";

	//export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	//export let loading_status: LoadingStatus | undefined = undefined;
	//export let value_is_output = false;
	export let interactive: boolean;
	export let rtl = false;
	export let loading_status: LoadingStatus;
	export let root: string;
	//export let show_download_button: boolean;
	export let container = true;
	//export let root: string;

    export let gradio: Gradio<{
		change: never;
		upload: never;
		clear: never;
        input: never;
        submit: never;
	}>;

    /* Constants */
    const dispatch = createEventDispatcher();

    
	let upload: Upload;
	let uploading = false;
    let el: HTMLTextAreaElement | HTMLInputElement;    

    let textarea: HTMLTextAreaElement;

    // Function to adjust textarea height
    function adjustTextareaHeight() {
        if (textarea) {
            // Reset the height to auto to get the correct scrollHeight for the current content
            textarea.style.height = 'auto';
            // Set the height to scrollHeight to accommodate all content
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    }

    // Call adjustTextareaHeight on mount and whenever textValue changes
    onMount(adjustTextareaHeight);
    $: textValue, adjustTextareaHeight();

                
    /* Functions */
    export let value_is_output = false;

    function handle_change(): void {
		gradio.dispatch("change");
		if (!value_is_output) {
			gradio.dispatch("input");
		}
	}

    function handle_submits(): void{
        console.log(textValue);
        console.log(images);
        
        // Dispatch the custom event with text and images data
        // dispatch('submit', submitData);
        value = { "text": textValue, "images": images };
        console.log(value);
        gradio.dispatch("submit");

        textValue = ""; // Reset the textValue
        images = []; // Clear the images array
        gradio.dispatch("clear");

    }


    async function handle_keypress(e: KeyboardEvent): Promise<void> {
        await tick();

        // Shift+Enter is pressed for a new line in textarea
        if (e.key === "Enter" && e.shiftKey) {
            // Allow the new line behavior by not preventing the default action
            // No need to explicitly insert a new line because 
            // a textarea will naturally handle Shift+Enter as a new line.
        } else if (e.key === "Enter") { // Enter alone is pressed for submit
            e.preventDefault(); // Prevents the default action to avoid submitting the form or inserting a new line
            
            handle_submits();
        }
    }


    function uploadFile(files: FileData[]) {
		console.log(files);

		// Convert files to pseudo FileData type and add to images array
		files.forEach(file => {
			// Assume FileData accepts a blob but needs to manage UI-related properties like 'type'
			// Create a URL for the file for UI use
			
			//const url = file.mime_type.startsWith('image/') ? URL.createObjectURL(file) : null;
			
			const type = file.orig_name.split('.').pop();
            console.log(file.mime_type);
			file.mime_type = type;
			// Adapt this part if you have a method to instantiate FileData directly from a File object
			// Construct an object that looks like FileData but includes necessary UI information
			const fileData = file;
			// Add the constructed object to your `images` array
			images = [...images, fileData];
		});

		dispatch('filesAdded', images);
		gradio.dispatch("upload");

    }

    function removeImage(index) {
        images.splice(index, 1);
        images = images.slice(); // trigger reactivity
        dispatch('imageRemoved', images);
    }

    /* Reactive statements */
    $: if (textValue === null) textValue = "";

    // When the value changes, dispatch the change event via handle_change()
    // See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
    $: textValue, handle_change();

	$: value, gradio.dispatch("change");

	let dragging: boolean;

</script>


<div class="text-image-uploader">
    <Block
        {visible}
        {elem_id}
        {elem_classes}
        {scale}
        {min_width}
        allow_overflow={false}
        padding={true}
    >

        <div class:image-previews={true} class:image-hidden={images.length === 0}>
            {#each images as image, index}
                    <div class="image-preview">
                            <ImagePreview
                            value = {image}
                            label = {''}
                            show_label = {false}
                            show_download_button = {false}
                            i18n={gradio.i18n}
                        />
                        <RemoveFile
                            on:remove_file={() => {
                                removeImage(index);
                                dispatch("clear");
                            }}
                        />
                    </div>
            {/each}
        </div>

        <div class:text-input-container={container}>
            <textarea
                data-testid="textbox"
                class="text-input"
                bind:value={textValue}
                bind:this={textarea}
                placeholder="Type here..."
                disabled={!interactive}
                dir={rtl ? "rtl" : "ltr"}
                on:keydown={handle_keypress} 
            ></textarea>


			<Block
                {visible}
                variant={"solid"}
                border_mode={dragging ? "focus" : "base"}
                padding={false}
                elem_id = {"upload-block-id"}
                elem_classes = {["upload-block-class"]}
                allow_overflow={false}
                {container}
                width = {50}
                height = {50}
            >
                <StatusTracker
                    autoscroll={gradio.autoscroll}
                    i18n={gradio.i18n}
                    {...loading_status}
                />
                <UploadHandler
                    bind:value={tempFile}
                    {root}
                    on:clear={() => gradio.dispatch("clear")}
                    on:drag={({ detail }) => (dragging = detail)}
                    on:upload={() => {
                        uploadFile(tempFile);
                        }}
                    show_label = {false}
                >
                    <UploadButton i18n={gradio.i18n} type="file"/>
                </UploadHandler>
            </Block>

        </div>

    </Block>

</div>


<style>

    /* Adjusted styles for the textarea to resemble the original input */
    .text-input {
        display: block;
        position: relative;
        outline: none !important;
        box-shadow: var(--input-shadow);
        background: var(--input-background-fill);
        padding: var(--input-padding);
        width: 100%;
        height: fit-content;
        color: var(--body-text-color);
        font-weight: var(--input-text-weight);
        font-size: var(--input-text-size);
        line-height: var(--line-sm);
        border: none;
        resize: none; /* Prevent resizing the textarea */
        overflow-y: auto; /* Enable vertical scroll if needed */
    }

    .text-image-uploader {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
    }

    .text-image-uploader .image-hidden {
        display: none;
    }


    .image-previews {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 10px;
    }
    
    .image-preview {
            position: relative;
    }

    .text-input-container {
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
    }
</style>