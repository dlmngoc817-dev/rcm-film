from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / 'app.py')

def test_discovery_flow_and_stale_results():
    app = AppTest.from_file(APP, default_timeout=20).run()
    assert not app.exception
    app.multiselect(key='seeds').set_value(['1']).run()
    app.button(key='recommend').click().run()
    assert not app.exception
    results = app.session_state['result_bundle'][1]
    assert len(results) == 10
    assert all(r['title'] != 'Interstellar' for r in results)
    app.text_input(key='mood').set_value('robots').run()
    assert not app.exception
    assert not any('films for your next' in item.value for item in app.subheader)

def test_empty_selection_and_unmatched_query():
    app = AppTest.from_file(APP, default_timeout=20).run()
    app.button(key='recommend').click().run()
    assert len(app.warning) == 1 and not app.exception
    app.text_input(key='mood').set_value('qzxwvvv').run()
    app.button(key='recommend').click().run()
    assert not app.exception
    assert app.session_state['result_bundle'][1] == []
