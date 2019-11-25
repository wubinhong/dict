<template>
    <v-content>
        <div>
            <div>
                <h2>Setting sub page</h2>
                <p>{{msg}}</p>
            </div>
        </div>
    </v-content>
</template>

<script>
export default {
    data: () => {
        return {
            msg: "个人设置"
        };
    }
};
</script>
