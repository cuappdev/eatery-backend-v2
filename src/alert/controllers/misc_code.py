# EateriesFromDB
"""alerts=EateriesFromDB.alerts(serialized_eatery["id"], serialized_alerts),

@staticmethod
    def alerts(eatery_id: int, serialized_alerts: list[dict]):
        return [
            EateriesFromDB.alert_from_serialized(alert)
            for alert in serialized_alerts
            if alert["eatery"] == eatery_id
        ]

    @staticmethod
    def alert_from_serialized(serialized_alert: dict):
        return EateryAlert(
            id=serialized_alert["id"],
            description=serialized_alert["description"],
            start_timestamp=serialized_alert["start_timestamp"],
            end_timestamp=serialized_alert["end_timestamp"],


    alerts = AlertStore.objects.filter(
            end_timestamp__gte=datetime.now().timestamp(),
            start_timestamp__lte=datetime.now().timestamp(),
        )
        serialized_alerts = AlertStoreSerializer(data=alerts, many=True)
        serialized_alerts.is_valid()
        )"""
