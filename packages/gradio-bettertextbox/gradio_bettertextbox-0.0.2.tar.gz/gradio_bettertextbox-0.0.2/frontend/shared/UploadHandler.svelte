<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import { BlockLabel } from "@gradio/atoms";
	import { Image as ImageIcon } from "@gradio/icons";

	import { Upload } from "@gradio/upload";
	import type { FileData } from "@gradio/client";
	import RemoveFile from "./RemoveFile.svelte";

	export let value: null | FileData;
	export let label: string | undefined = undefined;
	export let show_label: boolean;
	export let root: string;

	let upload: Upload;
	let uploading = false;

	function handle_upload({ detail }: CustomEvent<FileData>): void {
		value = detail;
		dispatch("upload");
		value = null;
		dispatch("clear");
	}
	$: if (uploading) value = null;

	const dispatch = createEventDispatcher<{
		change?: never;
		clear?: never;
		drag: boolean;
		upload?: never;
	}>();

	let dragging = false;
	$: dispatch("drag", dragging);
</script>

<BlockLabel {show_label} Icon={ImageIcon} label={label || "Image"} />

<div data-testid="image" class="image-container">
	{#if value?.url}
		<RemoveFile
			on:remove_file={() => {
				value = null;
				dispatch("clear");
			}}
		/>
	{/if}
	<div class="upload-container">
		<Upload
			hidden={value !== null}
			bind:this={upload}
			bind:uploading
			bind:dragging
			filetype="*/*"
			file_count='multiple'
			on:load={handle_upload}
			on:error
			{root}
		>
			{#if value === null}
				<slot />
			{/if}
		</Upload>
	</div>
</div>

<style>
	.image-frame :global(img) {
		width: var(--size-full);
		height: var(--size-full);
		object-fit: cover;
	}

	.image-frame {
		object-fit: cover;
		width: 100%;
		height: 100%;
	}

	.upload-container {
		height: 100%;
		flex-shrink: 1;
		max-height: 100%;
	}

	.image-container {
		display: flex;
		height: 100%;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		max-height: 100%;
	}
</style>
