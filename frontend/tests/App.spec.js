import { mount } from "@vue/test-utils";
import App from "../src/App.vue";  // Use relative path (avoid error)
import axios from "axios";
import MockAdapter from "axios-mock-adapter";

// Using Vue Test Utils and Jest to test the App component
describe("App.vue", () => {
  let mock;

  beforeEach(() => {
    mock = new MockAdapter(axios);
  });

  afterEach(() => {
    mock.restore();
  });

  it("renders the input textarea and button", () => {
    const wrapper = mount(App);
    expect(wrapper.find("textarea").exists()).toBe(true);
    expect(wrapper.find("button").exists()).toBe(true);
  });

  it("summarizes text when button is clicked", async () => {
    mock.onPost("http://127.0.0.1:8000/summarize").reply(200, {
      summary: "This is a test summary.",
    });

    const wrapper = mount(App);
    await wrapper.setData({ text: "Test input text" });

    await wrapper.find("button").trigger("click");

    await wrapper.vm.$nextTick();
    await new Promise((resolve) => setTimeout(resolve, 50)); // Ensure state updates (avoid error)

    expect(wrapper.text()).toContain("This is a test summary.");
  });
});
