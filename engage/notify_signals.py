from notifications.signals import notify

def send_direct_offer_notification(marketer, do):
    notify.send(sender=marketer, recipient=do.creator, action_object=do, verb='Successful Direct offer')
    print("Notification Sent!")
    return True