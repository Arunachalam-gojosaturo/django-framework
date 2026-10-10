function telemetryConsole() {
    return {
        wsConnected: false,
        socket: null,
        events: [],
        stats: {
            totalIngested: 0,
            totalDispatched: 0,
            successRate: 100,
            avgLatency: 14.2,
        },
        modalOpen: false,
        activeItem: {},
        isSimulating: false,

        init() {
            this.connectWebSocket();
            this.loadInitialMetrics();
        },

        connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const socketUrl = `${protocol}//${window.location.host}/ws/telemetry/demo-org/`;

            try {
                this.socket = new WebSocket(socketUrl);

                this.socket.onopen = () => {
                    this.wsConnected = true;
                    console.log("[PulseStream] WebSocket connected to", socketUrl);
                };

                this.socket.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        this.handleIncomingTelemetry(data);
                    } catch (e) {
                        console.warn("[PulseStream] Received non-JSON packet:", event.data);
                    }
                };

                this.socket.onclose = () => {
                    this.wsConnected = false;
                    console.log("[PulseStream] WebSocket disconnected. Reconnecting in 3s...");
                    setTimeout(() => this.connectWebSocket(), 3000);
                };

                this.socket.onerror = (err) => {
                    console.warn("[PulseStream] WebSocket connection notice:", err);
                    this.wsConnected = false;
                };
            } catch (err) {
                console.warn("[PulseStream] Direct WebSocket setup failed, running fallback simulation mode.");
            }
        },

        handleIncomingTelemetry(packet) {
            const now = new Date();
            const timeStr = now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0');

            if (packet.type === 'event_ingested') {
                this.stats.totalIngested++;
                this.events.unshift({
                    time: timeStr,
                    event_type: packet.event_type,
                    target: 'Ingestion Buffer',
                    status: 'INGESTED',
                    http_code: 202,
                    latency: 1.2,
                    raw: packet
                });
            } else if (packet.type === 'delivery_attempt') {
                this.stats.totalDispatched++;
                this.events.unshift({
                    time: timeStr,
                    event_type: packet.event_type,
                    target: packet.target_url || packet.endpoint_name || 'Webhook Target',
                    status: packet.status || 'DELIVERED',
                    http_code: packet.http_status_code || 200,
                    latency: packet.latency_ms || 18.5,
                    raw: packet
                });
            }

            // Cap buffer at 100 entries to prevent memory buildup
            if (this.events.length > 100) {
                this.events.pop();
            }
        },

        async loadInitialMetrics() {
            try {
                const resp = await fetch('/api/v1/dispatch/metrics/');
                if (resp.ok) {
                    const data = await resp.json();
                    this.stats.totalDispatched = data.total_dispatches || 0;
                    this.stats.successRate = data.success_rate_percent || 100;
                    this.stats.avgLatency = data.avg_latency_ms || 12.4;
                }
            } catch (e) {
                // Initial load silent catch
            }
        },

        async simulateEvent() {
            this.isSimulating = true;
            const sampleTypes = [
                'order.checkout_completed',
                'payment.captured',
                'customer.subscription_renewed',
                'inventory.threshold_low',
                'security.mfa_enrolled'
            ];
            const randomType = sampleTypes[Math.floor(Math.random() * sampleTypes.length)];
            const idempotencyKey = 'sim_' + Date.now() + '_' + Math.random().toString(36).substring(2, 9);

            const payloadData = {
                event_type: randomType,
                idempotency_key: idempotencyKey,
                payload: {
                    reference_id: "ref_" + Math.floor(Math.random() * 90000 + 10000),
                    currency: "USD",
                    amount: (Math.random() * 250 + 10).toFixed(2),
                    metadata: {
                        source: "operator_console",
                        region: "us-east-1"
                    }
                }
            };

            try {
                const response = await fetch('/api/v1/events/ingest/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payloadData),
                });

                if (response.ok) {
                    const resData = await response.json();
                    // If websocket is offline, record locally for immediate feedback
                    if (!this.wsConnected) {
                        const now = new Date();
                        const timeStr = now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0');
                        this.stats.totalIngested++;
                        this.stats.totalDispatched++;
                        this.events.unshift({
                            time: timeStr,
                            event_type: resData.event_type,
                            target: 'https://api.subscriber-crm.com/v1/webhooks',
                            status: 'DELIVERED',
                            http_code: 200,
                            latency: (Math.random() * 25 + 5).toFixed(1),
                            raw: resData
                        });
                    }
                }
            } catch (err) {
                console.error("[PulseStream] Error simulating event:", err);
            } finally {
                this.isSimulating = false;
            }
        },

        inspectPayload(item) {
            this.activeItem = item.raw || item;
            this.modalOpen = true;
        },

        clearEvents() {
            this.events = [];
        }
    };
}
