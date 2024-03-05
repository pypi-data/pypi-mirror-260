<svelte:options accessors={true} />

<script context="module" lang="ts">
	export { default as BaseImageUploader } from "./shared/UploadHandler.svelte";
	export { default as BaseStaticImage } from "./shared/UploadHandler.svelte";
	export { default as BaseExample } from "./Example.svelte";
    
</script>

<script lang="ts">
    import type { Gradio } from "@gradio/utils";
	import ImagePreview from "./shared/ImagePreview.svelte";
    import RemoveFile from "./shared/RemoveFile.svelte";
    import { Upload, ModifyUpload } from "@gradio/upload";
	import UploadHandler from "./shared/UploadHandler.svelte";

    import { Block, BlockTitle} from '@gradio/atoms';
	import { StatusTracker} from "@gradio/statustracker";
    import { tick } from "svelte";
    import UploadButton from "./shared/UploadButton.svelte";
    import { createEventDispatcher, onMount } from 'svelte';
    
    import { Image as ImageIcon } from '@gradio/icons';

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
                
    /* Functions */
    export let value_is_output = false;

    function handle_change(): void {
		gradio.dispatch("change");
		if (!value_is_output) {
			gradio.dispatch("input");
		}
	}

    async function handle_keypress(e: KeyboardEvent): Promise<void> {
        await tick();
        // console.log(e.key);

        if (e.key === "Enter") {
            e.preventDefault();
            
            console.log(textValue);
            console.log(images);
            
            // Dispatch the custom event with text and images data
            // dispatch('submit', submitData);
            value = { "text": textValue, "images": images };
            console.log(value);

            gradio.dispatch("submit");
        }
    }

    function uploadFile(files: FileData[]) {
		console.log(files);

		// Convert files to pseudo FileData type and add to images array
		files.forEach(file => {
			// Assume FileData accepts a blob but needs to manage UI-related properties like 'type'
			// Create a URL for the file for UI use
			
			//const url = file.mime_type.startsWith('image/') ? URL.createObjectURL(file) : null;
			
			const type = file.orig_name.split('.').pop()
			file.mime_type = type
			// Adapt this part if you have a method to instantiate FileData directly from a File object
			// Construct an object that looks like FileData but includes necessary UI information
			const fileData = file
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
            <input
                data-testid="textbox"
                type="text"
                class="scroll-hide"
                bind:value={textValue}
                bind:this={el}
                placeholder="Type here..."
                disabled={!interactive}
                dir={rtl ? "rtl" : "ltr"}
                on:keypress={handle_keypress}
            />
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
	input {
		display: block;
		position: relative;
		outline: none !important;
		box-shadow: var(--input-shadow);
		background: var(--input-background-fill);
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
	}
	/* .container > input {
		border: var(--input-border-width) solid var(--input-border-color);
		border-radius: var(--input-radius);
	} */

	input:disabled {
		-webkit-text-fill-color: var(--body-text-color);
		-webkit-opacity: 1;
		opacity: 1;
	}

	input:focus {
		box-shadow: var(--input-shadow-focus);
		border-color: var(--input-border-color-focus);
	}

	input::placeholder {
		color: var(--input-placeholder-color);
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

    .image-preview button {
            position: absolute;
            top: 0;
            right: 0;
    }

    .text-input-container {
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
    }

    /* .text-input-container textarea {
            flex-grow: 1;
            resize: vertical;
    } */

    .add-button {
    padding: 8px 16px;
    background-color: #2d333b;
    /* border: 1px solid #ccc; */
    border-radius: 4px;
    font-size: 24px;
    cursor: pointer;
  }

  .add-button:hover {
    background-color: #e0e0e0;
  }

</style>