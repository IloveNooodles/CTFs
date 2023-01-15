<script lang="ts">
	import { fade, blur } from "svelte/transition";
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<div class="flex flex-col justify-center items-center text-center">
		<span class="block absolute w-[100%] top-[35%]">
			<h1>
				<p in:fade={{ duration: 500, delay: 0 }}>
					Welcome to <br />
					TCP1P Node Package Generator
				</p>
			</h1>
			<a href="/playground" in:blur={{ delay: 300 }}>click here to play</a
			>
		</span>
	</div>
</section>
