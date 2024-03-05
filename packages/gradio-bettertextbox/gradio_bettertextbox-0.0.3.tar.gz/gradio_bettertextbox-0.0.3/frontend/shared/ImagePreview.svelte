<script lang="ts">
	import { BlockLabel, Empty, IconButton } from "@gradio/atoms";
	import { Download } from "@gradio/icons";
	import { DownloadLink } from "@gradio/wasm/svelte";
	import { type ComponentType } from "svelte";
	import { Image as ImageIcon } from "@gradio/icons";
	import { type FileData } from "@gradio/client";
	import type { I18nFormatter } from "@gradio/utils";
	import FileIcon from './FileIcon.svelte';

	export let value: null | FileData;

	export let label: string | undefined = undefined;
	export let show_label: boolean;
	export let show_download_button = true;
	export let selectable = false;
	export let i18n: I18nFormatter;


	function truncateFilename(filename: string, maxLength: number = 20): string {
		if (!filename) return '';
		if (filename.length <= maxLength) return filename;
		return `${filename.substring(0, maxLength - 3)}...`;
	}

	function removeFileTypeAddon(filename:string){
		return filename.split('/').pop();
	}

	const extensions = ["jpg", "jpeg", "png", "bmp", "gif", "svg", "webp"];
</script>

<BlockLabel
	{show_label}
	Icon={ImageIcon}
	label={label || i18n("image.image")}
/>
{#if value === null}
  <Empty unpadded_box={true} size="large"><ImageIcon /></Empty>
{:else if extensions.includes(value.mime_type)} <!-- Check if the file is an image -->
  <div class="icon-buttons">
    {#if show_download_button}
      <DownloadLink href={value.url} download={value.orig_name || "image"}>
        <IconButton Icon={Download} label={i18n("common.download")} />
      </DownloadLink>
    {/if}
  </div>
  <button>
    <div class:selectable class="image-container">
      <img src={value.url} alt="" loading="lazy" />
    </div>
  </button>
{:else} <!-- Non-image file -->
  <button>
    <div class="file-type-container">
			<button
				on:click
				class = "uploaded-File-icon"
			>
				<FileIcon value={removeFileTypeAddon(value.mime_type)} />
		</button>
		<p style="font-size:x-small">{truncateFilename(value.orig_name, 15)}</p> 
    </div>
  </button>
{/if}

<style>
	.image-container :global(img),
	button {
		width: 75px;
		height: 75px;
		object-fit: contain;
		display: block;
		border-radius: var(--radius-lg);
	}

	.selectable {
		cursor: crosshair;
	}

	.icon-buttons {
		display: flex;
		position: absolute;
		top: 6px;
		right: 6px;
		gap: var(--size-1);
	}
</style>
