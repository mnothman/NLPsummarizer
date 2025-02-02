module.exports = {
    moduleFileExtensions: ["js", "json", "vue"],
    transform: {
      "^.+\\.vue$": "@vue/vue3-jest",
      "^.+\\.js$": "babel-jest"
    },
    moduleNameMapper: {
      "^@/(.*)$": "<rootDir>/src/$1"
    },
    testEnvironment: "jsdom",
    transformIgnorePatterns: ["/node_modules/(?!(axios)/)"]
  };
  