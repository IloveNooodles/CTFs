<script>
    import { page } from "$app/stores";
</script>

<section>
    <div class="flex flex-col justify-center items-center text-center">
        <span class="block absolute w-[100%] top-[45%]">
            <h1>{$page.error?.message}</h1>
        </span>
    </div>
</section>
