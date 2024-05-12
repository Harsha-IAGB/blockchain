class MQTT:
    keepalive = 60
    port = 1883
    server = "18.212.190.136"

class BlockParameters:
    max_transactions = 3

class GPubSub:
    credentials_file = "/Users/sriharshavarahabhatla/Desktop/courses/ENPM693-NetworkSecurity/gcp-pubsub-private-key.json"

    class Topic:
        class TransactionAdd:
            subscription_path = "projects/nomadic-botany-422915-m7/subscriptions/transaction-add"
            topic_path = "projects/nomadic-botany-422915-m7/topics/transaction-add"

        class BlockAdd:
            subscription_path = "projects/nomadic-botany-422915-m7/subscriptions/block-add-sub"
            topic_path = "projects/nomadic-botany-422915-m7/topics/block-add"
