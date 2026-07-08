import unittest

from agents.analyzer import analyzer_agent
from agents.optimizer import optimizer_agent
from agents.parser import parser_agent


class GreetingFlowTests(unittest.TestCase):
    def test_hi_short_circuits_pipeline(self):
        state = parser_agent({"query": "hi"})

        self.assertTrue(state.get("is_greeting"))
        self.assertEqual(state.get("tables"), [])
        self.assertEqual(state.get("columns"), [])
        self.assertEqual(state.get("issues"), [])
        self.assertEqual(
            state.get("suggestion"),
            "Hi! Please share a SQL query you'd like to optimize.",
        )
        self.assertEqual(analyzer_agent(state), state)
        self.assertEqual(
            optimizer_agent(state, {"llm": {"model": "unused", "temperature": 0}}),
            state,
        )

    def test_non_greeting_query_keeps_existing_flow(self):
        parsed = parser_agent({"query": "SELECT id FROM users"})

        self.assertIsNone(parsed.get("is_greeting"))
        self.assertIn("users", parsed.get("tables", []))
        analyzed = analyzer_agent(parsed)
        self.assertIn("Missing WHERE clause", analyzed.get("issues", []))


if __name__ == "__main__":
    unittest.main()
