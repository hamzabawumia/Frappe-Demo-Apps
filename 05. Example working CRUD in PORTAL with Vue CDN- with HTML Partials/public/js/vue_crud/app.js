/* Connect the generic Composition API to the Portal page. */
const { createApp, onMounted } = Vue;

createApp({
    setup() {
        const crud = useCrud(config);
        onMounted(() => crud.loadObjects());
        return { config, ...crud };
    }
}).mount("#app");
