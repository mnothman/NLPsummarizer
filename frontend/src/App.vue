<template>
  <div id="app">
    <h1>Text Summarizer</h1>
    <textarea v-model="text" placeholder="Enter text to summarize..." rows="5" cols="50"></textarea>
    <br />
    <button @click="summarizeText">Summarize</button>
    <div v-if="summary">
      <h3>Summary:</h3>
      <p>{{ summary }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      text: "",
      summary: "",
    };
  },
  methods: {
    async summarizeText() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/summarize", {
          text: this.text,
        });
        this.summary = response.data.summary;
      } catch (error) {
        console.error("Error summarizing text:", error);
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  padding: 20px;
}
textarea {
  margin: 10px 0;
  width: 100%;
}
button {
  padding: 10px 20px;
  cursor: pointer;
}
</style>
