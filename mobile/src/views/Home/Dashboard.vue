<template>
    <v-content>
        <div>
            <div>
                <h2>Dashboard sub page</h2>
            </div>
            <HelloWorld />
        </div>
    </v-content>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";

export default {
    // name: "Dashboard",
    components: {
        HelloWorld
    }
};
</script>
