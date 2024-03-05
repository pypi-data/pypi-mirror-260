<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import { IconButton } from "@gradio/atoms";
	import { Clear } from "@gradio/icons";

	const dispatch = createEventDispatcher();
</script>

<div>
	<IconButton
		Icon={Clear}
		label="Remove File"
		on:click={(event) => {
			dispatch("remove_file");
			event.stopPropagation();
		}}
	/>
</div>

<style>
	div {
		display: flex;
		position: absolute;
		top: var(--size-2);
		right: var(--size-2);
		justify-content: flex-end;
		gap: var(--spacing-sm);
		z-index: var(--layer-5);
	}
</style>
