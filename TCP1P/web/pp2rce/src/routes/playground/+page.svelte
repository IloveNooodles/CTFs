<script lang="ts">
	import { onMount } from "svelte";
	import { slide } from "svelte/transition";
	let output = "";
	let input = JSON.stringify(
		{
			version: "1.0.0",
			scripts: {
				production: "node app.js",
			},
			foo: "bar",
		},
		null,
		"\t"
	);
	async function get() {
		const res = await fetch("/api/generator", {
			method: "POST",
			body: JSON.stringify({
				js: input,
			}),
			headers: {
				"Content-Type": "Aplication/json",
			},
		});
		const res_json = await res.json();
		input = JSON.stringify(JSON.parse(input), null, "\t");
		output = JSON.stringify(res_json, null, "\t");
	}
	onMount(() => {
		get();
	});
</script>

<svelte:head>
	<title>playground</title>
	<meta name="description" content="json playground" />
</svelte:head>

<section transition:slide>
	<h1>Node Package Generator</h1>
	<div class="flex flex-row">
		<div class="text-black w-[50%]">
			<textarea
				class="p-5 resize-none w-[100%] h-[100%]"
				name="input"
				id="input"
				cols="30"
				rows="18"
				bind:value={input}
			/>
		</div>
		<div class="w-1" />
		<div class="w-[50%] text-black">
			<textarea class="p-5 w-[100%] h-[100%]">{output}</textarea>
		</div>
	</div>
	<div class="flex justify-center content-center p-2">
		<button
			class="w-[100%] bg-blue-700 rounded p-2 hover:bg-blue-500"
			on:click={get}>SEND</button
		>
	</div>
</section>
