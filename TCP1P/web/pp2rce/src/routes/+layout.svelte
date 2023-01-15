<script>
	import Header from "./Header.svelte";
	import "../app.css";
	import "./styles.css";
</script>

<div class="flex flex-col min-h-[100vh]">
	<Header />
	<main
		class="flex-1 flex flex-col p-[1rem] w-[100%] max-w-[64rem] m-auto box-border"
	>
		<slot />
	</main>

	<footer class="flex flex-col content-center items-center p-[12px]">
		<p>
			don't forget to visit <a class="font-bold" href="https://ctf.tcp1p.com"
				>ctf.tcp1p.com</a
			>
		</p>
	</footer>
</div>