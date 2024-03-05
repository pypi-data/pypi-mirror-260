
<script lang="ts">
	import type { I18nFormatter } from "@gradio/utils";

    export let value: string = "";

</script>

<svg
xmlns="http://www.w3.org/2000/svg"
width="100%"
height="100%"
viewBox="0 0 24 24"
fill="none"
stroke="currentColor"
stroke-width="1.5"
stroke-linecap="round"
stroke-linejoin="round"
>
<path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
<polyline points="13 2 13 9 20 9" />
<!-- Adding "PDF" text -->
<text x="7.5" y="17" fill="currentColor" style="stroke-width: 0.2; font-size: 6; font-family: Arial, sans-serif; letter-spacing: 0.3; color: red;">{value}</text>
</svg>