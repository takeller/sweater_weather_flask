def assert_payload_type(obj, payload, field, data_type):
    obj.assertIn(field, payload)
    obj.assertIsInstance(payload[field], data_type)